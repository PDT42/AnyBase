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
        },
        secondary: {
            light: '#E6F9AF',
            main: '#8BBEB2',
            dark: '#384E77',
            contrastText: '#000',
        },
    },
});

let indexPage = (
    <ThemeProvider theme={theme}>
        <BasePage />
    </ThemeProvider>
);

// Render Index Page
// =================
ReactDOM.render(indexPage, document.getElementById("root"));
