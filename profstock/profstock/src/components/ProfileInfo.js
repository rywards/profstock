import React from 'react';
import axios from 'axios';

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