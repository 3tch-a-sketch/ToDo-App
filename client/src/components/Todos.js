import React from 'react'
import Todo from './Todo.js'

const Todos = ({todos, deleteTodo, changeComplete}) => {
  return (
    <div>
        {todos.map((todo) => {
            return <Todo key={todo.id} title={todo.title} done={todo.done} id={todo.id} deleteTodo={deleteTodo} changeComplete={changeComplete}/>
        })}
    </div>
  )
}

export default Todos
