import { useRef, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import user_logo from './assets/user_icon.png';
import bot_logo from './assets/bot_icon.png';
import settings_logo from './assets/settings.png';
import send_logo from './assets/send-button.png';

function App() {
  const navigate = useNavigate();
  const [isopen, setOpen] = useState(false);
  const [user_msg, setUser_msg] = useState("");
  const [show_user_text, setShow_user_text] = useState([]);
  const [show_bot_text, setShow_bot_text] = useState([]);
  const chatRef = useRef(null);
  function open() {
    console.log("settings clicked");
    setOpen(!isopen)
  }
  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, [show_bot_text, show_user_text])
  async function send_user_msg() {
    if (!user_msg.trim()) {
      return;
    }
    const current_msg = user_msg;
    setShow_user_text([...show_user_text, current_msg]);
    setUser_msg("")

    const response = await fetch(
      "https://ai-agentic-desktop-assistant.onrender.com/usermsg",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          "user_msg": current_msg
        })
      }
    )
    const data = await response.json();
    setShow_bot_text([...show_bot_text, data["bot_msg"]])
  }

  return (
    <>
      <div className="title">
        <h1><center>DESKO-ASSIST</center></h1>
        <button className="settings_button" onClick={open}>
          <img src={settings_logo} className="settings" width={70} alt="" />
        </button>
      </div>
      {isopen &&
        <div className="open_settings">
          <button className="bar-buttons">
            <h1>About</h1>
          </button>
          <button className="bar-buttons">
            <h1>Theme</h1>
          </button>
          <button className="bar-buttons">
            <h1>Chat History</h1>
          </button>
          <button className="bar-buttons">
            <h1>Profile</h1>
          </button>
          <button className="bar-buttons">
            <h1>Laptop-Access</h1>
          </button>
          <button className="bar-buttons">
            <h1>Chat History</h1>
          </button>
          <button className="bar-buttons">
            <h1>Chat History</h1>
          </button>
          <button className="bar-buttons" onClick={() => navigate("/about")}>
            <h1>About</h1>
          </button>
          <button className="bar-buttons">
            <h1>Logout</h1>
          </button>
          <button className="bar-buttons" onClick={() => navigate("/updates")}  >
            <h1>Updates</h1>
          </button>
        </div>
      }
      <div className="chat-area" ref={chatRef}>
        {show_user_text.map((msg, index) => (
          <div key={index}>
            <div className="user">
              <img src={user_logo} width={100}></img>
              <p>{msg}</p>
            </div>
            {show_bot_text[index] && (
              <div className="bot">
                <img src={bot_logo} width={100}></img>
                <p>{show_bot_text[index]}</p>
              </div>
            )}
          </div>
        ))}
      </div>
      <div className="msg-area">
        <div className="chatbot-msg-box">
          <textarea
            className="msg-box"
            value={user_msg}
            onChange={(e) => {
              setUser_msg(e.target.value);
              if (e.target.value) {
                e.target.style.height = 'auto';
                e.target.style.height = e.target.scrollHeight + 'px';
              }
            }}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                send_user_msg();
                setTimeout(() => {
                  e.target.style.height = '30px'
                }, 0)
              }
            }}
            rows={1}
            style={{ resize: 'none', overflow: 'hidden', minHeight: '40px' }}></textarea>
        </div>
        <button className="send-button" onClick={() => { send_user_msg(); }}><img src={send_logo} className="arrow-img" width={50}></img></button>
      </div>
    </>

  );
}
export default App;