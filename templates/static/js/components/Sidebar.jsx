import React, { Component } from "react";
import { Drawer } from "@material-ui/core";
import { withStyles } from "@material-ui/core/styles";
import Input from '@material-ui/core/Input';
import { Dialog, DialogTitle, DialogContent, Button, TextField, DialogActions } from "@material-ui/core";
import { List, ListItem, ListItemIcon, ListItemSecondaryAction, ListItemText } from '@material-ui/core';
import IconButton from '@material-ui/core/IconButton';
import MoreVertIcon from '@material-ui/icons/MoreVert';
import AddIcon from '@material-ui/icons/Add';
import CloseIcon from '@material-ui/icons/Close';
import { CirclePicker } from 'react-color'
import Menu from '@material-ui/core/Menu';
import MenuItem from '@material-ui/core/MenuItem';

const drawerWidth = 300;
const navHeight = 64;

const styles = theme => ({
    drawer: {
        marginTop: navHeight,
        width: drawerWidth,
        flexShrink: 0,
    },
    drawerPaper: {
        marginTop: navHeight,
        width: drawerWidth,
        padding: theme.spacing(3),
    },
    input: {
        marginBottom: theme.spacing(8),
    },
    check: {
        minWidth: 10,
    },
    addButton: {
        position: 'absolute',
        right: theme.spacing(5),
        top: theme.spacing(20),
    },
    closeButton: {
        position: 'absolute',
        right: theme.spacing(1),
        top: theme.spacing(1),
    },

    listItem: {
        height: 40,
        width: '100%',
        maxWidth: 360,
        backgroundColor: theme.palette.background.paper,
        paddingLeft: 0,
    },

    textBox: {
        marginBottom: 30,
    },

    colourPicker: {
        marginBottom: 30,
    },
    colourPreview: {
        width: 16,
        height: 16,
        borderRadius: 4,
        marginRight: 13,
    },
});

class Sidebar extends Component {  
    constructor(props) {
        super(props);
	    this.state = {nlpText: ""}
        this.handleNlpCreation = this.handleNlpCreation.bind(this);
    }

    componentDidMount() {
        this.getCalList()
    }

    handleNlpCreation(e) {
        console.log(e.target.value)
        const response = fetch('/getIntent', {
          method: 'POST',
          body: JSON.stringify({"nlpText": e.target.value}),
          headers: {
            'Content-Type': 'application/json;charset=utf-8'
          }
        }).then(response => response.json()).then(data => this.props.handleNlpData(data))
    }

    deleteCal(calendar) {
        console.log("i am being called")
        let updatedCalendars = this.props.calendars.filter (
            cal => cal["name"] !== calendar.name
        );
        let deletedCalendar = this.props.calendars.filter (
            cal => cal["name"] === calendar.name
        );
        //this.setState({ events: updatedEvents });
        this.delete_calendar(deletedCalendar[0])
    }

    delete_calendar(calendar) {
        let response = fetch('/deleteCalendar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
        body: JSON.stringify({"name": calendar.name, "colour": calendar.colour})
        }).then((data) => data.json()).then(data => {
            if (data.success) {
                // append to events list
                // this.setState({ events: [], calendars: [] })
                // this.get_calendars()
                console.log("Suceeededdddd")
            } else {
                console.log("Failedddddddd")
            }
        });
    }

    getCalList() {
        let response = fetch('/getEvents', {
            method: 'GET'
        }).then((data) => data.json()).then(data => this.renderCalList(data));
    }

    handleDots(name) {
        console.log(name)
    }

    renderCalList(calList) {
        var new_list = new Array()
        for (var i = 0 ; i < calList.calendars.length ; i++) {
            new_list.push(calList.calendars[i])
        }
        this.render()
        this.forceUpdate()
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
              }}>
                <h3>Add a Quick Event</h3>
                <Input
                  className={classes.input}
                  placeholder="Lunch at 2pm tomorrow"
                  inputProps={{
                    'aria-label': 'description',
                  }}
                  value={ this.props.nlpText }
                  onChange={e => {
                    this.props.setNlpBarState(e.target.value)
                  }}
                  onKeyPress={ e => {
                    if (e.key === "Enter") {
                      this.handleNlpCreation(e)
                    }
                  }}/>
                <div>
                    <h3>My Calendars</h3>
                    <IconButton className={classes.addButton} edge="end" onClick={this.props.handleCreateOpen}>
                        <AddIcon />
                    </IconButton>
                </div>
                <List>
                {this.props.calendars.map(item => {
                    const labelId = `cal-${item.name}`;
                    return (
                        <div>
                            <ListItem className={classes.listItem} key={item.name} dense button>
                                <div style={{backgroundColor: `${item.colour}`}} className={classes.colourPreview}></div>
                                <ListItemText id={labelId} primary={`${item.name}`} />
                                    <ListItemSecondaryAction>
                                        <IconButton edge="end" aria-label="comments" onClick={this.props.handleClick, this.handleDots.bind(this, `${item.name}`)}>
                                            <MoreVertIcon />
                                        </IconButton>
                                    </ListItemSecondaryAction>
                                </ListItem>
                                {/* Menu for each calendar */}
                                <Menu
                                anchorEl={this.props.anchorEl}
                                keepMounted
                                open={Boolean(this.props.anchorEl)}
                                onClose={this.props.handleClose}>
                                <MenuItem onClick={this.props.handleClose}>Edit</MenuItem>
                                <MenuItem>Delete</MenuItem>
                            </Menu>
                      </div>
                    );
                    })}
                    </List>

                {/* Modal to create new calendar */}
                <Dialog maxWidth = {'md'} open={this.props.createPopUp} onClose={this.props.handleClose}>
                    <IconButton aria-label="close" className={classes.closeButton} onClick={this.props.handleClose}>
                        <CloseIcon />
                    </IconButton>
                    <DialogTitle className={this.title} id="customized-dialog-title" onClose={this.props.handleClose}>
                        Create a new calendar
                    </DialogTitle>
                    <DialogContent>
                        <TextField
                          className={classes.textBox}
                          placeholder="Calendar Name"
                          margin="dense"
                          onChange={e => {
                            this.props.setCalName(e.target.value);
                          }}/>
                        <CirclePicker
                          className={classes.colourPicker}
                          color={ this.props.colour }
                          onChangeComplete={ this.props.setCalColour }/>
                    </DialogContent>
                    <DialogActions>
                        <Button
                          label="Create Contact"
                          variant="contained"
                          color="primary"
                          onClick={() => {
                            this.props.setNewCalendar(), this.props.handleClose();
                          }}>
                        Create Calendar
                        </Button>
                    </DialogActions>
                </Dialog>
            </Drawer>
        );
    }
}

export default withStyles(styles)(Sidebar);
