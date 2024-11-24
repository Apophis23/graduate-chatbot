const BASE_URL = import.meta.env.VITE_API_URL;

async function createChat() {
  const res = await fetch(BASE_URL + '/chats', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  });
  const data = await res.json();
  if (!res.ok) {
    return Promise.reject({ status: res.status, data });
  }
  return data;
}

async function sendChatMessage(chatId, message, file) {
  const formData = new FormData();
  formData.append('message', message);
  if (file) {
    formData.append('file', file);
  }

  const res = await fetch(BASE_URL + `/chats/${chatId}`, {
    method: 'POST',
    body: formData
  });

  if (!res.ok) {
    return Promise.reject({ status: res.status, data: await res.json() });
  }
  return res.body;
}

export default {
  createChat,
  sendChatMessage
};