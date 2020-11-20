import React, { Component } from 'react';
import axios from 'axios';

class Home extends Component {
  constructor(props) {
    super(props);
    this.state = { value: '' };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({ value: event.target.value });
  }

  handleSubmit(event) {
    console.log(typeof ({ "query": this.state.value }));
    var query = { "query": this.state.value };
    axios.post("http://localhost:8090/search", query).then(token => {
      console.log(token);
      console.log(token.data);

      var imageElems = []
      for(var i = 0; i < token.data.length; i++){
        var img = document.createElement('img')
      }

    });
    // console.log(response);
    event.preventDefault();
  }

  render() {

    return (
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center"
        }}
      >
        <form onSubmit={this.handleSubmit}>
          <label>
            Image Search
          <input type="text" value={this.state.value} onChange={this.handleChange} />
          </label>
          <input type="submit" value="Submit" />
        </form>
      </div>

    );
  }
}

export default Home