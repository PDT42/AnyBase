import React from 'react';
import ReactDOM from 'react-dom';
import { createMuiTheme, ThemeProvider } from "@material-ui/core";
import './index.css';
import reportWebVitals from './reportWebVitals';
import { BasePage } from './pages/base-page';

let theme = createMuiTheme({
  typography: {
    fontSize: 12,
  },
  palette: {
    primary: {
      main: '#18314F',
      dark: '#0D0630',
      contrastText: '#FFF'
    },
    secondary: {
      main: '#E6F9AF',
      dark: '#8BBEB2',
      contrastText: '#000',
    }
  }
});

ReactDOM.render(
  <ThemeProvider theme={theme}>
    <BasePage />
  </ThemeProvider>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
