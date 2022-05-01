import { useState, useEffect } from 'react'
import Control from './components/Control.js'
import Todos from './components/Todos.js'
import "./GlobalStyle.css"



function App() {


  // window.addEventListener('load', getTodos)
  useEffect( () => { // this functions exactly like the code above but is the 'react' way of doing it
    getTodos()
  }, [])

  function changeComplete(id, done){
    // TODO: change this so that it updates the todo in the database

    let change = todos.find(todo => todo.id === id)
    todos.splice(todos.indexOf(change), 1)
    change.done = done

    todos.push(change)
    setTodos(todos)
  }

  function deleteTodo(id){
    // TODO: change this so that it deletes the todo from the server
    setTodos(todos.filter(todo => todo.id !== id))
  }
  function deleteMultipleTodos(id){
    setTodos(todos.filter(todo => !id.includes(todo.id)))
  }
  function addTodo(title){
    // TODO: change this so that it adds the todo to the server
    
    setTodos([...todos, {id: todos.length+1, title: title, done: false}])
  }

  function getTodos(){
    var xhr = new XMLHttpRequest()
    xhr.addEventListener('load', () => {
      let json = JSON.parse(xhr.responseText)
      let jsonArray = [];

      for(let key in json){
        jsonArray.push(json[key])
      }
      setTodos(jsonArray)
    })

    if(window.location.hostname === 'localhost'){
      // console.log('running locally')
      xhr.open('GET', 'http://127.0.0.1:8000/todo')
    }else{
      alert("this code has not been tested check console")
      xhr.open('GET', "http://"+window.location.hostname+':8000/todo')
      console.log(window.location.hostname)
    }

    xhr.send()

  }

  const [todos, setTodos] = useState([{id: 1, title: "default", done: false}])


  return (
    <div className="App">
      <Control todos={todos} deleteMultipleTodos={deleteMultipleTodos} deleteTodo={deleteTodo} addTodo={addTodo} />
      
      <Todos todos={todos} deleteTodo={deleteTodo} changeComplete={changeComplete}></Todos>
    </div>
  );
}

export default App;
