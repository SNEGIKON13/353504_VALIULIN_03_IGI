import React, { Component } from 'react';
import Main from './components/MainComponent';
import './App.css';
import { BrowserRouter } from 'react-router-dom';
import { Provider } from 'react-redux';
import { ConfigureStore } from './redux/configureStore';

const store = ConfigureStore();

class App extends Component {

  render(){
    return (
      <Provider store={store}>
        <BrowserRouter>
          <div>
            <Main />
          </div>
        </BrowserRouter>
      </Provider>
    );
  }

}

export default App;

/**
 * Run legacy version:
 * "start": "react-scripts --openssl-legacy-provider start"
 * instead of:
 * "start": "react-scripts start"
 * source: https://stackoverflow.com/a/69713899
 */
