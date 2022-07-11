import React, { useContext } from "react";
import { useNavigate } from "react-router-dom";

import { AuthContext } from "../../context";
import HeaderButton_v1 from "../UI/Button/HeaderButton/HeaderButton_v1";

const AppHeader = () => {
    const {isAuth, setIsAuth} = useContext(AuthContext)
    const redirect = useNavigate()
    let buttons_context = []

    const ExitEvent = (event) => {
        localStorage.clear()
        setIsAuth(false)
        redirect('/lk')
    }
    const RegisterEvent = (event) => {
        redirect('/register')
    }
    const LoginEvent = (event) => {
        redirect('/login')
    }
    const HomeEvent = (event) => {
        redirect('/lk')
    }

    if (isAuth == false) {
        buttons_context = [
            {className: 'HeaderWorkArea__Button', 
             'name': 'Регистрация', 'link': false, 
             'eventHandler': RegisterEvent},
            {className: 'HeaderWorkArea__Button',
             'name': 'Авторизация', 'link': false, 
             'eventHandler': LoginEvent},
            {className: 'HeaderWorkArea__Button',
             'name': 'Домой', 'link': false, 
             'eventHandler': HomeEvent}
        ]
    } else if (isAuth == true) {
        buttons_context = [
            {className: 'HeaderWorkArea__Button', 
             'name': 'Домой', 'link': false, 
             'eventHandler': HomeEvent},
            {className: 'HeaderWorkArea__Button', 
             'name': 'Выход', 'linl': false, 
             'eventHandler': ExitEvent}
        ]   
    }
    
    const header_buttons = buttons_context.map((item, index) => 
        <HeaderButton_v1 key={index} context={item} />
    )
    return (
        <div className="AllHeaderBox__HeaderWorkArea HeaderWorkArea">
            {header_buttons}
        </div>
    )
}

export default AppHeader