import React, { useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../../context";

import HeaderButton_v1  from '../../components/UI/Button/HeaderButton/HeaderButton_v1'
import { addMoney } from "../../utils/HomeActionTool/HomeActionTool";

const MyHome = () => {
    const redirect = useNavigate()
    let {isAuth, setIsAuth} = useContext(AuthContext)
    useEffect(() => {
        if (isAuth == false) {
            redirect('/login')
        }
    })

    let getBalanceEvent = (event) => {
        redirect('/my_balance')
    }

    let getTransactEvent = (event) => {
        redirect('/transact')
    }

    let getMyTransactionsList = (event) => {
        redirect('/my_transactions')
    }

    let addMoneyEvent = (event) => {
        addMoney()
    }

    const actionButtons_context = [
        {className: 'ActionBox__ActionButton', 
         name: 'Узнать сой баланс', 
         eventHandler: getBalanceEvent},
        {className: 'ActionBox__ActionButton', 
         name: 'Совершить перевод по номеру телефона', 
         eventHandler: getTransactEvent},
        {className: 'ActionBox__ActionButton', 
         name: 'Просмотреть истроию своих переводов', 
         eventHandler: getMyTransactionsList},
        {className: 'ActionBox__ActionButton', 
         name: 'Добавить 5000р', 
         eventHandler: addMoneyEvent}
    ]
    
    let actionButtons = actionButtons_context.map((item, index) => 
        <HeaderButton_v1 key={index} context={item}/>)

    return (
        <div className="AllContentBox__ContentWorkArea ContentWorkArea">
            <div className="ContentWorkArea__AboutBox AboutBox">
                <p className="AboutBox__text">Вы попали на страницу самого лучшего банка на планете.</p>
                <p className="AboutBox__text">Наш банк предоставляет уникальную услугу, перевод по номеру телефона!</p>
                <p className="AboutBox__text">Да-да вы не ослышались, Телефон по номеру Перевода!</p>
                <p className="AboutBox__text">У нас самая лучшая планета в банке</p>
                <div className="AboutBox__delimiter"></div>
            </div>
            <div className="ContentWorkArea__ActionsBox ActionBox">
                <h1 className="ActionBox__title">
                    Доступные функции
                </h1>
                {actionButtons}
            </div>
        </div>
    )
}

export default MyHome