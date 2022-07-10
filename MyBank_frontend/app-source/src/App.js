import React, { useState, useEffect } from 'react';
import { BrowserRouter } from 'react-router-dom';

import { AuthContext } from './context/index';
import AppHeader from './components/AppHeader/AppHeader'
import AppFooter from './components/AppFooter/AppFooter'
import AppRouter from './router/AppRouter';
import { checkAccessToken, request_for_refresh_token } from './utils/authTools'
import './App.css';

function App() {
  const [isAuth, setIsAuth] = useState(null)

  async function authentication() {
    const access = localStorage.getItem('access')
    const refresh = localStorage.getItem('refresh')
    if (access) {
      let result = await checkAccessToken(access)
      if (result) {
        return true
      } else if (refresh) {
        let result =  await request_for_refresh_token(refresh)
        if (result) {
          return true
        }
      } 
    } 
  }

  if (isAuth == null) {
    authentication().then((result) => {
      console.log(result)
      if (result) {
        setIsAuth(true)
      } else {
        setIsAuth(false)
      }
    })
  }
  return (
    <AuthContext.Provider value={{isAuth, setIsAuth}}>
      <BrowserRouter>
      <div className='AllDocumentBox'>
        <div className='AllHeaderBox'>
          <AppHeader />
        </div>
        <div className='AllContentBox'>
          <AppRouter />
        </div>
        <div className='AllFooterBox'>
          <AppFooter />
        </div>
      </div>
      </BrowserRouter>
    </AuthContext.Provider>
  );
}
export default App;
