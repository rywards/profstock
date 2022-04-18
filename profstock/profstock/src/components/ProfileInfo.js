import React from 'react';
import axios from 'axios';

<>
<script src="https://unpkg.com/react@17/umd/react.development.js" crossorigin></script>
<script src="https://unpkg.com/react-dom@17/umd/react-dom.development.js" crossorigin></script>
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
</>

export default class PersonList extends React.Component {
  state = {
    persons: []
  }

  componentDidMount() {
    axios.get(`https://jsonplaceholder.typicode.com/users`)
      .then(res => {
        const persons = res.data;
        this.setState({ persons });
      })
  }

  render() {
    return (
        this.state.persons
            .map(person =>
                <ul id='pfpdisplayinfo'>
           
                    <li id="ProfileName" key={person.name}></li>
                    <li id="ProfileSubInfo" key={person.email}></li>
                </ul>
        )
    )
  }
}