import { createMuiTheme, ThemeProvider } from "@material-ui/core";
import ReactDOM from "react-dom";

import "./index.css";
import { BasePage } from "./pages/base-page";

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
        },
        danger: {
            main: '#ad180a',
            contrastText: '#FFF'
        }
    }
});

let indexPage = (
    <ThemeProvider theme={theme}>
        <BasePage />
    </ThemeProvider>
);

// Render Index Page
// =================
ReactDOM.render(indexPage, document.getElementById("root"));
