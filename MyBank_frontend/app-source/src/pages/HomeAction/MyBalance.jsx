import React, { useContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../../context";
import { myBalance } from '../../utils/HomeActionTool/HomeActionTool'

const MyBalance = () => {
    let redirect = useNavigate()
    let {isAuth, setIsAuth} = useContext(AuthContext)
    let [balance, setBalance] = useState(null)

    useEffect(() => {
        if (isAuth == false) {
            redirect('/login')
        }
    })
    if (isAuth == true && balance == null) {
        console.log(isAuth)
        console.log(balance)
        let access_token = localStorage.getItem('access')
        myBalance(access_token).then(balance => {
            setBalance(balance) // 100 | false
        })
    }
    console.log('pererender')
    return (
        <div className="AllContentBox__ContentWorkArea ContentWorkArea">
            <div className="ContentWorkArea__MyInfoBox MyInfoBox">
                <div className="MyInfoBox__MyBalance">
                    {isAuth == null 
                    ? <p>Загрузка...</p>
                    : <p>Ваш баланс: {balance} р</p>
                    }
                </div>
            </div>
        </div>
    );
};

export default MyBalance;