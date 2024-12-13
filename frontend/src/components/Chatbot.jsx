import { useState } from 'react';
import { useImmer } from 'use-immer';
import api from '@/api';
import { parseSSEStream } from '@/utils';
import ChatMessages from '@/components/ChatMessages';
import ChatInput from '@/components/ChatInput';

function Chatbot() {
  const [chatId, setChatId] = useState(null);
  const [messages, setMessages] = useImmer([]);
  const [newMessage, setNewMessage] = useState('');
  const [file, setFile] = useState(null);

  const isLoading = messages.length && messages[messages.length - 1].loading;

  async function submitNewMessage() {
    const trimmedMessage = newMessage.trim();
    if (!trimmedMessage || isLoading) return;

    setMessages(draft => [...draft,
      { role: 'user', content: trimmedMessage },
      { role: 'assistant', content: '', sources: [], loading: true }
    ]);
    setNewMessage('');

    let chatIdOrNew = chatId;
    try {
      if (!chatId) {
        const { id } = await api.createChat();
        setChatId(id);
        chatIdOrNew = id;
      }

      const stream = await api.sendChatMessage(chatIdOrNew, trimmedMessage, file);
      for await (const textChunk of parseSSEStream(stream)) {
        setMessages(draft => {
          draft[draft.length - 1].content += textChunk;
        });
      }
      setMessages(draft => {
        draft[draft.length - 1].loading = false;
      });
    } catch (err) {
      console.log(err);
      setMessages(draft => {
        draft[draft.length - 1].loading = false;
        draft[draft.length - 1].error = true;
      });
    } finally {
      setFile(null); // 파일 전송 후 초기화
    }
  }

  return (
    <div className='relative grow flex flex-col gap-6 pt-6'>
      {messages.length === 0 && (
        <div className='mt-3 font-urbanist text-primary-grey text-xl font-light space-y-2'>
          <p>👋 안녕하세요!</p>
          <p>졸업사정 챗봇 <b>Easy Grad</b>입니다. 포털시스템에 참고용 성적표를 다운로드하여 입력하시면 졸업 관련 사항을 안내드립니다!</p>
          <p><b>인하대학교 포털시스템 : </b> <a href="https://portal.inha.ac.kr/login.jsp?idpchked=false" target="_blank"><b className='text-primary-navy'>여기</b></a>를 눌러주세요!</p>
          <p>현재 소프트웨어융합대학을 대상으로 서비스 중입니다!</p>
          <p>사용법을 알고 싶으시다면 '사용법 알려줘'와 같이 입력해 보세요!</p>
        </div>
      )}
      <ChatMessages
        messages={messages}
        isLoading={isLoading}
      />
      <ChatInput
        newMessage={newMessage}
        isLoading={isLoading}
        setNewMessage={setNewMessage}
        setFile={setFile}
        submitNewMessage={submitNewMessage}
      />
    </div>
  );
}

export default Chatbot;
