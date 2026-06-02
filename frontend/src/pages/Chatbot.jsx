
import { useState, useEffect } from "react";

import axios from "axios";

function Chatbot() {

    const [file, setFile] = useState(null);

    const [question, setQuestion] = useState("");

    const [messages, setMessages] = useState([]);
    const [history, setHistory] = useState([]);

    useEffect(() => {

        loadHistory();

    }, []);

    const loadHistory = async () => {

        const email =
            localStorage.getItem("email");

        const response =
            await axios.get(
                `https://rag-backend-0bjx.onrender.com/history/${email}`
            );

        setHistory(
            response.data
        );

    } 




const askQuestion = async () => {

    if (!file) {

        alert("Please upload PDF");

        return;
    }

    if (!question) {

        alert("Please ask question");

        return;
    }

    const userMessage = {

        sender: "user",

        text: question
    };

    setMessages((prev) => [

        ...prev,

        userMessage
    ]);

    try {

        const email =
            localStorage.getItem("email");

        const formData = new FormData();

        // IMPORTANT FIX
        formData.append(
            "question",
            question
        );

        formData.append(
            "email",
            email
        );

        formData.append(
            "file",
            file
        );



        const response = await axios.post(

            "https://rag-backend-0bjx.onrender.com/chat",

            formData,

            {
                headers: {
                    "Content-Type":
                        "multipart/form-data"
                }
            }
        );

        const botMessage = {

            sender: "bot",

            text: response.data.answer
        };

        setMessages((prev) => [

            ...prev,

            botMessage
        ]);

        setQuestion("");

    } catch (error) {

        console.log(error);

        const botMessage = {

            sender: "bot",

            text:
                error.response?.data?.answer ||
                "Backend Error"
        };

        setMessages((prev) => [

            ...prev,

            botMessage
        ]);
    }
};



return (

    <div
        style={{
            display: "flex",
            height: "100vh"
        }}
    >

        {/* Sidebar */}

        <div
            style={{
                width: "250px",
                borderRight: "1px solid #ccc",
                padding: "15px",
                overflowY: "auto"
            }}
        >

            <h3>Chat History</h3>

            {
                history.map(
                    (chat, index) => (

                        <div
                            key={index}

                            style={{
                                padding: "10px",
                                marginBottom: "10px",
                                background: "#f2f2f2",
                                borderRadius: "5px"
                            }}
                        >
                            {chat.question}
                        </div>

                    )
                )
            }

        </div>

        {/* Main Chat */}

        <div
            style={{
                flex: 1,
                padding: "20px"
            }}
        >

            <h1>
                AI PDF Chatbot 🤖
            </h1>

            <input
                type="file"
                accept=".pdf"
                onChange={(e) =>
                    setFile(
                        e.target.files[0]
                    )
                }
            />

            <br /><br />

            <div
                style={{

                    border: "1px solid gray",

                    minHeight: "400px",

                    padding: "20px",

                    borderRadius: "10px",

                    overflowY: "auto"
                }}
            >

                {
                    messages.map(
                        (msg, index) => (

                            <div
                                key={index}

                                style={{

                                    textAlign:
                                        msg.sender === "user"
                                            ? "right"
                                            : "left",

                                    marginBottom: "20px"
                                }}
                            >

                                <div
                                    style={{

                                        display: "inline-block",

                                        padding: "12px",

                                        borderRadius: "10px",

                                        background:
                                            msg.sender === "user"
                                                ? "#cfe2ff"
                                                : "#e2e2e2",

                                        maxWidth: "70%"
                                    }}
                                >

                                    <b>
                                        {
                                            msg.sender === "user"
                                                ? "You"
                                                : "Bot"
                                        }
                                        :
                                    </b>

                                    <br />

                                    {msg.text}

                                </div>

                            </div>
                        )
                    )
                }

            </div>

            <br />

            <input
                type="text"

                placeholder="Ask question about PDF..."

                value={question}

                onChange={(e) =>
                    setQuestion(
                        e.target.value
                    )
                }

                style={{
                    width: "400px",
                    padding: "10px"
                }}
            />

            <button

                onClick={askQuestion}

                style={{
                    marginLeft: "10px",
                    padding: "10px"
                }}
            >
                Send
            </button>


        </div>
    </div>

);
}


export default Chatbot;

