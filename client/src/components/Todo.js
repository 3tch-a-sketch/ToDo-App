import React, {useRef} from 'react'

const Todo = ({title, done, deleteTodo, id, changeComplete}) => {
  let complete = useRef()

  function deleteTodoButton(){
    console.log("deleting todo")
    deleteTodo(id)
  }
  function toggleComplete(e){
    // e.overrideDefault()
    console.log("toggling todo")
    changeComplete(id, !done)
    complete.current.checked = !done
    done = !done
  }

  return (
    <div style={style}>
      <input style={checkBox} type="checkbox" defaultChecked={done} ref={complete} onClick={toggleComplete}></input>
      <span>{title}</span>
      <span onClick={deleteTodoButton} style={cross} > ❌</span>
    </div>
  )
}

Todo.defaultProps = {
    title: "default title",
    done: false
}

const style={
    border: "1px solid black",   
    padding: "10px",
    margin: "1px",
}

const cross={
    float: "right",
    cursor: "pointer",
}

const checkBox={
    float: "left",
    padding: "10px",
    
}
 
export default Todo
