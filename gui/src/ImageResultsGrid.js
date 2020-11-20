import React, { Component } from 'react';
// import { makeStyles } from '@material-ui/core/styles';
// import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';
import history from './history';
import axios from 'axios';

// const useStyles = makeStyles((theme) => ({
//   root: {
//     '& > *': {
//       margin: theme.spacing(1),
//     },
//   },
//   input: {
//     display: 'none',
//   },
// }));

export default class ImageResultsGrid extends Component {

  state = {
    loading: false,
    value: ''
  };

  // const classes = useStyles();

  handleInputChange({target}) {
    this.setState({
      [target.name]: target.value
    });
  }

  handleSubmit = async event => {
    this.handleSearch(event.target.value);
    this.setState({value: event.target.value});
  }

  handleSearch = async value => {

    // eslint-disable-next-line no-template-curly-in-string
    axios.get('http://http://0.0.0.0:8080/?caption=${value}')
      .then(response => {
        console.log(response.data);
        return (
          <img src={response.data}/>
        )
      })
      .catch(error => console.log(error))
  };

  render() {
    return (
      
      <Grid container spacing={2} justify="center">
      <div>
      <Button 
          variant="contained" 
          color="primary" 
          onClick={() => history.push('/')}
      >
        Back
      </Button>
      <form>
        <br/><br/>
            <br/><br/>
            <header><h1>Image Recog</h1></header>
            
            
            <br/>
            <input
              value={this.state.value}
              onChange={event => this.handleSubmit(event)}
              placeholder="Enter an identifier"
            />
            <Button 
                variant="contained" 
                color="primary" 
                onClick={event => this.handleSubmit(event)}
            >
              Submit
            </Button>
            
            </form>
      </div>
      </Grid>
    );
  }
}