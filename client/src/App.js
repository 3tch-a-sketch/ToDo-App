import { useState, useEffect } from 'react'
import Control from './components/Control.js'
import Todos from './components/Todos.js'
import "./GlobalStyle.css"
import axios from 'axios'

const apiUrl = 'http://'+window.location.hostname+':8000/todo/'


function App() {
  

  // window.addEventListener('load', getTodos)
  useEffect( () => { // this functions exactly like the code above but is the 'react' way of doing it
    getTodos()
  }, [])

  function changeComplete(id, done){

    // let change = todos.find(todo => todo.id === id)
    // todos.splice(todos.indexOf(change), 1)
    // change.done = done

    // todos.push(change)
    // setTodos(todos)
    let idPos = todos.findIndex(todo => todo.id === id)

    axios.put(apiUrl, {id: id, done: done, title: todos[idPos].title})


  }

  function deleteTodo(id){
    // setTodos(todos.filter(todo => todo.id !== id))
    
    axios.delete(apiUrl, { data: { id: id }}).then(res => {
      console.log(res)
      getTodos()
    })

  }
  function deleteMultipleTodos(ids){
    // setTodos(todos.filter(todo => !id.includes(todo.id)))

    for(let i = 0; i < ids.length; i++){
      deleteTodo(ids[i])
    }

  }
  function addTodo(title){
    
    // setTodos([...todos, {id: todos.length+1, title: title, done: false}])
    axios.post(apiUrl, {
      title: title,
    }).then(res => {
      getTodos()
      console.log(res)
    }).catch(err => {
      console.log(err)
    })
  }

  function getTodos(){
    axios.get(apiUrl).then(res => {
      let jsonArray = [];

      for(let key in res.data){
        jsonArray.push(res.data[key])
      }
      // console.log(jsonArray)
      setTodos(jsonArray)
    })
  }
  
  const [todos, setTodos] = useState([{id: 1, title: "default", done: false}])


  return (
    <div className="App">
      {/* <button onClick={getTodos}>Force update</button>
      <button onClick={testPost}>test POST</button> */}
      <Control todos={todos} deleteMultipleTodos={deleteMultipleTodos} deleteTodo={deleteTodo} addTodo={addTodo} />
      <Todos todos={todos} deleteTodo={deleteTodo} changeComplete={changeComplete}></Todos>
    </div>
  );
}


export default App;
