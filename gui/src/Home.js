import React, { Component } from 'react';
import Button from '@material-ui/core/Button';
import history from './history';
import Grid from '@material-ui/core/Grid';

class Home extends Component {
  render() {

    return (
      <Grid container spacing={2} justify="center">
      <div>
      
      <form>
        <br/><br/>
            <br/><br/>
            <header><h1>Image Recog</h1></header>
            
            
            <br/>
              <Button 
                  variant="contained" 
                  color="primary" 
                  onClick={() => history.push('/ImageUploadResults')}>
                Upload a photo
              </Button>
              <Button 
                  variant="contained" 
                  color="primary" 
                  onClick={() => history.push('/ImageResultsGrid')}>
                Search the database
              </Button>
              <br/>
              </form>
      </div>
      </Grid>
    );
  }
}

export default Home