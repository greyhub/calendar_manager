import React, { Component } from 'react';
import { Route } from 'react-router-dom';
import Login from './components/Login';
import Activities from './components/Activities';
import './App.css';
import BasicTable from './components/BasicTable'
// import AppBar from '@mui/material/AppBar';
// import Box from '@mui/material/Box';
// import Toolbar from '@mui/material/Toolbar';
// import Typography from '@mui/material/Typography';
// import Button from '@mui/material/Button';
// import IconButton from '@mui/material/IconButton';
// import * from '@mui/icons-material';
// import * as React from 'react';

class App extends Component {
  render() {
    return (
      <div>
        <div className="header">
          <a className="logo">CTSV</a>
          <div className="header-right">
            <a className="active" href="/">Home</a>
            {/* <a href="#contact">Contact</a> */}
            <a href="/activities">Activities</a>
          </div>
        </div>

        {/* <div style="padding-left:20px">
          <h1>Responsive Header</h1>
          <p>Resize the browser window to see the effect.</p>
          <p>Some content..</p>
        </div> */}
        <div className="container">
          {/* <Box sx={{ flexGrow: 1 }}>
          <AppBar position="static">
            <Toolbar>
              <IconButton
                size="large"
                edge="start"
                color="inherit"
                aria-label="menu"
                sx={{ mr: 2 }}
              >
                <MenuIcon />
              </IconButton>
              <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                News
              </Typography>
              <Button color="inherit">Login</Button>
            </Toolbar>
          </AppBar>
        </Box> */}

          <Route exact path="/" component={Login} />
          <Route path="/activities" component={Activities} />
        </div>
        <footer className="footer-distributed">

          <div className="footer-left">

            <h3>CT<span>SV</span></h3>

            <p className="footer-company-name">CTSV &copy; 2022</p>
          </div>

          <div className="footer-center">

            <div>
              <i className="fa fa-map-marker"></i>
              <p><span>1 Dai Co Viet Street</span> Hanoi, Vietnam</p>
            </div>



          </div>

          <div className="footer-right">

            <p className="footer-company-about">
              <span>About CTSV</span>
              
            </p>



          </div>

        </footer>
      </div>

    );
  }
}

export default App;
