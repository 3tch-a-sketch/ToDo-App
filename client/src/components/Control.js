import React, {useRef} from 'react'
import "./ControlStyle.css"

const Control = ({ todos, deleteTodo, addTodo , deleteMultipleTodos}) => {

    let todoName = useRef()

    function purgeCompleted(){
        // console.log("purging completed")
        console.log(todos)
        let deleteLater = []
        for(let i = 0; i < todos.length; i++){
            // console.log("checking", todos[i], i)
            if(todos[i].done === true){
                // deleteTodo(todos[i].id)
                deleteLater.push(todos[i].id)
            }
        }
        // console.log(deleteLater)
        
        deleteMultipleTodos(deleteLater)
        
    }
    function addTodoButton(){
        if(todoName.current.value === "") return
        addTodo(todoName.current.value)
        todoName.current.value = null
    }

  return (
    <div className='container' style={style}>
        <label>Title:</label>
        <input ref={todoName} ></input>
        <button onClick={addTodoButton}>Add</button>
        <button onClick={purgeCompleted}>Purge Completed</button>
    </div>
  )
}
let style = {
    // border: "1px solid black",
    padding: "10px",
    width: "400px",
}

export default Control
