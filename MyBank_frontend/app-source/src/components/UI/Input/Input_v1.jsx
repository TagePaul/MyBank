import React from "react";
import cl from './Input_v1.module.css'


const Input_v1 = (props) => {

    return (
        <input className={cl.Input_v1} {...props}></input>
    );
};

export default Input_v1