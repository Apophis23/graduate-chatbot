import Chatbot from '@/components/Chatbot';
import logo from '@/assets/images/Signature_LR01.png';
import easy_grad from '@/assets/images/easy_grad.svg'; 

function App() {
  const handleRefresh = () => {
    window.location.reload();
  };

  return (
    <div className='flex flex-col min-h-full w-full max-w-3xl mx-auto px-4'>
      <header className='sticky top-0 shrink-0 z-20 bg-white'>
        <div className='flex flex-col h-full w-full gap-1 pt-4 pb-2'>
          <a href='https://swcc.inha.ac.kr/act/index.do' target="_blank">
            <img src={logo} className='w-32' alt='logo' />
          </a>

          <img src={easy_grad} className='w-32 cursor-pointer' alt='Easy Grad' onClick={handleRefresh}/>
        </div>
      </header>
      <Chatbot />
    </div>
  );
}

export default App;
