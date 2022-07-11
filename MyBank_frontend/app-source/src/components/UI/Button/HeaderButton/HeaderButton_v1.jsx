import React from "react"

const HeaderButton_v1 = (props) => {
    return (
        <div className={props.context.className} 
             onClick={props.context.eventHandler}>
            {props.context.name}
        </div>
    )
}

export default HeaderButton_v1;