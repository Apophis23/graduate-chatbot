import { useRef } from 'react';
import useAutosize from '@/hooks/useAutosize';
import sendIcon from '@/assets/images/send.svg';

function ChatInput({ newMessage, setNewMessage, isLoading, submitNewMessage, setFile }) {
  const textareaRef = useAutosize(newMessage);
  const fileInputRef = useRef(null); // 파일 입력 필드에 접근하기 위한 ref 생성

  function handleKeyDown(e) {
    if (e.keyCode === 13 && !e.shiftKey && !isLoading) {
      e.preventDefault();
      handleSubmit();
    }
  }

  function handleFileChange(e) {
    setFile(e.target.files[0]); // 파일 상태 업데이트
  }

  function handleSubmit() {
    if (!isLoading) {
      submitNewMessage();
      setFile(null); // 파일 상태 초기화
      if (fileInputRef.current) {
        fileInputRef.current.value = ''; // 파일 입력 필드 초기화
      }
    }
  }

  return (
    <div className='sticky bottom-0 bg-white py-4'>
      <div className='p-1.5 bg-primary-blue/35 rounded-3xl z-50 font-mono origin-bottom animate-chat duration-400'>
        {/* 파일 입력 */}
        <div className="mb-2 flex items-center justify-between">
          <input
            type="file"
            ref={fileInputRef} // ref 연결
            className="block text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:bg-primary-blue/20 file:text-primary-grey hover:file:bg-primary-blue/30"
            onChange={handleFileChange}
          />
        </div>
        {/* 메시지 입력 */}
        <div className='pr-0.5 bg-white relative shrink-0 rounded-3xl overflow-hidden ring-primary-blue ring-1 focus-within:ring-2 transition-all'>
          <textarea
            className='block w-full max-h-[140px] py-2 px-4 pr-11 bg-white rounded-3xl resize-none placeholder:text-primary-blue placeholder:leading-4 placeholder:-translate-y-1 sm:placeholder:leading-normal sm:placeholder:translate-y-0 focus:outline-none'
            ref={textareaRef}
            rows='1'
            value={newMessage}
            onChange={e => setNewMessage(e.target.value)}
            onKeyDown={handleKeyDown}
          />
          <button
            className='absolute top-1/2 -translate-y-1/2 right-3 p-1 rounded-md hover:bg-primary-blue/20'
            onClick={handleSubmit}
          >
            <img src={sendIcon} alt='send' />
          </button>
        </div>
      </div>
    </div>
  );
}

export default ChatInput;
