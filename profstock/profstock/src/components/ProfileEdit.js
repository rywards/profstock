import React from 'react';
import axios from 'axios';

export default class UserEdit extends React.Component {
  state = {
    firstname: '',
    lastname: '',
    email: ''
  }

  handleFirstChange = event => {
    this.setState({ firstname: event.target.value });
  }
  handleSecondChange = event => {
      this.setState({ lastname: event.target.value});
  }
  handleThirdChange = event => {
    this.setState({email: event.target.value });
  }
  

  handleSubmit = event => {
    event.preventDefault();

    const user = {
      firstname: this.state.firstname,
      lastname: this.state.lastname,
      email: this.state.email
    };

    axios.post(`https://jsonplaceholder.typicode.com/users`, { user })
      .then(res => {
        console.log(res);
        console.log(res.data);
      })
  }

  render() {
    return (
        <div id='profileText'>
        <h2> Profile Info to Edit: </h2>
        <form onSubmit={this.handleSubmit}>
            <hr></hr>
            <br/>
            <br/>
            <label for="firstname">First name:</label>
            <input type="text" name="firstname" onChange={this.handleFirstChange}></input>
            <label for="lastname">Last name:</label>
            <input type="text" name="lastname" onChange={this.handleSecondChange}></input>
            <br/><br/>
            <hr></hr>
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" onChange={this.handleThirdChange}></input>
            <br/><br/>
            <hr></hr>
            <br/><br/>
            <hr></hr>
            <br/><br/>
            <hr></hr>
            <br/><br/>
            <input type="submit" id="pfpbutton" name="button"></input>
        </form>
    </div>
    )
  }
}