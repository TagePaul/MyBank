import React from 'react';
import { Routes, Route, Navigate} from "react-router-dom";

import Register from "../pages/Register/Register";
import Login from '../pages/Login/Login.jsx';
import MyHome from '../pages/MyHome/MyHome'
import Transact_v1 from '../pages/HomeAction/Transact/Transact'
import MyTransactions from '../pages/HomeAction/MyTransactions'
import MyBalance from '../pages/HomeAction/MyBalance';

const AppRouter = () => {
    return (
        <Routes>
            <Route path='/register' element={<Register/>}/>
            <Route path='/login' element={<Login/>}/>
            <Route path='/lk' element={<MyHome/>}/>
            <Route path='/transact' element={<Transact_v1 />}/>
            <Route path='/my_transactions' element={<MyTransactions />}/>
            <Route path='/my_balance' element={<MyBalance />}/>
            <Route path='*' element={<Navigate to='/lk'/>}/>
        </Routes>
    );
};

export default AppRouter