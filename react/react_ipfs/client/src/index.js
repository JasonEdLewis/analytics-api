import React, { Component, useEffect, useState} from 'react'
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
import getWeb3 from './utils/getWeb3'



const Index = () =>  {

  const [adress, setAdress ] = useState("")
  const persistor = persistStore(store);
  
  useEffect(()=>{
   return getWeb3().then((r)=> setAdress(r.currentProvider.selectedAddress))
  }, [])

    return (
      
        <React.StrictMode>
        <Provider store={store}>
        <PersistGate loading={null} persistor={persistor}>
      <div >
      <BrowserRouter>
        {adress && <Routes>
          <Route path="/" element={<Navigation/>}>
              <Route index element={<Home />} />
              <Route path="Experience" element={<App />} />
              <Route path="create" element={<CreateAlbum />} />
          </Route>
        </Routes>}
      </BrowserRouter>
      </div>
      </PersistGate>
      </Provider>
      </React.StrictMode>
    )
  
}


// export default function BaseApp (){
//   let theAlbumsURI
 

  // const getAlbumURI =() => {
  //  $.getJSON("https://ipfs.io/ipfs/QmVDa1UnYwLsb1YQe1Et5jLPNDQBJqoFqWfNBrH41Xxv21", (data)=> data).then((r) => 
  //  { 
  //    console.log(r)
  //    theAlbumsURI = r })
  // }

//  getAlbumURI()
   
//   console.log(theAlbumsURI)
    // const styles ={
       
    //     // border: '1px solid'
    // }
//     let persistor = persistStore(store);
//     return (
//       <React.StrictMode>
//       <Provider store={store}>
//       <PersistGate loading={null} persistor={persistor}>
//     <div style={styles}>
//     <BrowserRouter>
//       <Routes>
//         <Route path="/" element={<Navigation/>}>
//             <Route index element={<Home />} />
//             <Route path="Experience" element={<App />} />
//             <Route path="create" element={<CreateAlbum />} />
//         </Route>
//       </Routes>
//     </BrowserRouter>
//     </div>
//     </PersistGate>
//     </Provider>
//     </React.StrictMode>
//     )

// }

ReactDOM.render(<Index  />, document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
