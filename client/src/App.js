import React from 'react';
import socketIOClient from "socket.io-client";
import './App.css';


const ENDPOINT = "http://127.0.0.1:8100";
const RESOURCE = "resource1";


class App extends React.Component{
  constructor(props) {
    super(props);
    this.state = {logs: []}
  }

  scrollToBottom = () => {
    this.messagesEnd.scrollIntoView({ behavior: "smooth" });
  };

  componentDidMount() {
    this.socket = socketIOClient.connect(ENDPOINT, {
      reconnection: true
    });
    console.log("Component Mounted");
    this.socket.on("connect", () => {
      console.log("Connected to Server !!");
      this.socket.emit('client connection', RESOURCE);
    });
    this.socket.on("display static log", data => {
      console.log('Display Static Log');
      this.setState({
        logs: data
      })
    });
    this.socket.on("display log", data => {
      console.log('Display Log');
      this.setState({
        logs: [...this.state.logs, data]
      })
    });
  }

  componentDidUpdate(prevProps, prevState, snapshot) {
    this.scrollToBottom();
  }

  componentWillUnmount() {
    this.socket.emit('client disconnection', RESOURCE);
    console.log('Disconnected from Server !!');
    this.socket.close();
    console.log("Component Unmounted");
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <div className="Log-Container">
            <div>
              {this.state.logs.map(log => <p key={log.key}>{log.msg}</p>)}
            </div>
            <div style={{ float:"left", clear: "both" }}
                 ref={(el) => { this.messagesEnd = el; }}>
            </div>
          </div>
        </header>
      </div>
    );
  }
}

export default App;
