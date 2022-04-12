import React from 'react';
import ReactDOM from 'react-dom';
import * as serviceWorker from './serviceWorker';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { PersistGate } from 'redux-persist/integration/react';
import { persistStore } from 'redux-persist';
// import persistor from './configureStore'
import store from './app/store'
import { Provider } from 'react-redux'
import './index.css';
import Navigation from './components/Navigation';
import Home from './components/Home';
import App from './App';
import CreateAlbum from './components/CreateAlbum';


export default function BaseApp (){
    const styles ={
       
        // border: '1px solid'
    }
    let persistor = persistStore(store);
    return (
      <React.StrictMode>
      <Provider store={store}>
      <PersistGate loading={null} persistor={persistor}>
    <div style={styles}>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigation/>}>
            <Route index element={<Home />} />
            <Route path="Experience" element={<App />} />
            <Route path="create" element={<CreateAlbum />} />
        </Route>
      </Routes>
    </BrowserRouter>
    </div>
    </PersistGate>
    </Provider>
    </React.StrictMode>
    )

}

ReactDOM.render(<BaseApp  />, document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
