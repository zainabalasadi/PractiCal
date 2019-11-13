import React, { Component } from "react";
import { Drawer } from "@material-ui/core";
import { withStyles } from "@material-ui/core/styles";
import Input from '@material-ui/core/Input';

const drawerWidth = 300;

const styles = theme => ({
    drawer: {
        width: drawerWidth,
        flexShrink: 0,
    },
    drawerPaper: {
        width: drawerWidth,
        padding: theme.spacing(3),
    },
    toolbar: theme.mixins.toolbar,
    input: {
        marginBottom: theme.spacing(8),
    },
});



class Sidebar extends Component {  
    constructor() {
        super()
        this.state = {
            nlpText: ""
        }
        this.handleNlpCreation = this.handleNlpCreation.bind(this);
    }

    handleNlpCreation(e) {
        console.log(e.target.value)
        const response = fetch('/nlpCreation', {
          method: 'POST',
          body: JSON.stringify({"creationString": e.target.value}),
          headers: {
            'Content-Type': 'application/json;charset=utf-8'
          }
        }).then(response => response.json()).then(data => console.log(data))
        // TODO Insert code to reflect changes in back end on the front end given the 
        // response from the fetch request
    }

    render() {
        const { classes } = this.props;
        return (
            <Drawer
              className={classes.drawer}
              variant="permanent"
              anchor="right"
              classes={{
                paper: classes.drawerPaper,
              }}
            >
            <div className={classes.toolbar} />
                <h3>Add a Quick Event</h3>
                <Input
                  className={classes.input}
                  placeholder="Lunch at 2 tomorrow"
                  inputProps={{
                    'aria-label': 'description',
                  }}
                  value={ this.state.nlpText }
                  onChange={e => {
                    this.setState({ nlpText: e.target.value})
                  }}
                  onKeyPress={ e => {
                    if (e.key === "Enter") {
                      this.handleNlpCreation(e)
                    }
                  }}
                />
                <h3>My Calendars</h3>
            </Drawer>
        );
    }
}

export default withStyles(styles)(Sidebar);