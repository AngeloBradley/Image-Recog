import React, { Component } from 'react';
import axios from 'axios';
var fs = require("fs")

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
    axios.post("http://localhost:5000", query).then(token => {
      console.log(token);
      console.log(token.data);

      // for (var i = 0; i < token.data.length; i++) {
      //   var data = token.data[i].replace(/^data:image\/\w+;base64,/, "");
      //   var buf = new Buffer(data, 'base64');
      //   fs.writeFile('image' + i + '.jpg', buf, function (err, result) {
      //     if (err) { console.log('error', err); }
      //   });
      // }

    });
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