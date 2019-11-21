import React, { Component } from "react";
import { Drawer } from "@material-ui/core";
import { withStyles } from "@material-ui/core/styles";
import Input from '@material-ui/core/Input';
import { Dialog, DialogTitle, DialogContent, Button, TextField, Checkbox } from "@material-ui/core";
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
        top: theme.spacing(17),
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
        // TODO Insert code to reflect changes in back end on the front end given the 
        // response from the fetch request
    }

    create_calendar(calendar) {
        let response = fetch('/createCalendar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
        body: JSON.stringify({"name": calendar.name, "colour": calendar.colour})
        }).then((data) => data.json()).then(cal => {
            if (cal.success) {
                console.log("Created calendar successfully")
                this.state.calendars.push(calendar)
            } else {
                console.log("Failed calendar creation")
            }
        });
    }

    deleteCal(calendar) {
        let updatedCalendars = this.props.events.filter (
            cal => cal["name"] != calendar.name
        );
        this.delete_calendar(calendar)
    }

    delete_calendar(calendar) {
        let response = fetch('/deleteCalendar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
        body: JSON.stringify({"name": calendar.name, "colour": calendar.colour})
        }).then((data) => data.json()).then(cal => {
            if (cal.success) {
                let updatedCalendars = this.props.events.filter (
                    cal => cal["name"] !== calendar.name
                );
        
                this.setState({ calendar: updatedCalendars });
            } else {
                console.log("Failed calendar deleted")
            }
        });
    }

    getCalList() {
        let response = fetch('/getEvents', {
            method: 'GET'

        }).then((data) => data.json()).then(data => this.renderCalList(data));
    }

    renderCalList(calList) {
        var new_list = new Array()
        for (var i = 0 ; i < calList.calendars.length ; i++) {
                 new_list.push(calList.calendars[i])
        }

        //this.setState((prevState) => {
        //    calendars: Array.prototype.push.apply(prevState.calendars, new_list)
        //})

        this.render()
        this.forceUpdate()
    }

   getNotifList() {
        let response = fetch('/getNotifs', {
            method: 'GET'

        }).then((data) => data.json()).then(data => this.renderNotifList(data));
    }

    renderNotifList(calList) {
        var new_list1 = new Array()
        for (var i = 0 ; i < calList.length ; i++) {
                new_list1.push(calList[i])
        }

        this.setState((prevState) => {
            notifs: Array.prototype.push.apply(prevState.notifs, new_list1)
        })

        this.render()
        this.forceUpdate()
    }

   renderObject(){
    for (var i = 0 ; i < this.props.notifs.length ; i++) {
       return (
           this.renderNotifListsss(this.props.notifs[i])
       )
    }
   }

   renderNotifListsss(e) {
        console.log(e.title)
        return (
            <h10>
                {e.title}
                <br></br>
                {e.sender}
                <br></br>
                {e.start}
                <br></br>
                {e.type}
            </h10>
        )
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
                <h3>Add a Quick Event</h3>
                <Input
                  className={classes.input}
                  placeholder="Lunch at 2 tomorrow"
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
                  }}
                />
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
                        <ListItemIcon className={classes.check}>
                        </ListItemIcon>
                        <ListItemText id={labelId} primary={`${item.name}`} />
                            <ListItemSecondaryAction>
                                <IconButton edge="end" aria-label="comments" onClick={this.props.handleClick}>
                                    <MoreVertIcon />
                                </IconButton>
                            </ListItemSecondaryAction>
                        </ListItem>
                        {/* Menu for each calendar */}
                        <Menu
                        anchorEl={this.props.anchorEl}
                        keepMounted
                        open={Boolean(this.props.anchorEl)}
                        onClose={this.props.handleClose}
                      >
                          <MenuItem onClick={this.props.handleClose}>Edit</MenuItem>
                          <MenuItem /*onClick={this.props.deleteCal(item.name)}*/>Delete</MenuItem>
                      </Menu>
                      </div>
                    );
                    })}
                    </List>

                <h3>My Notifs</h3>
                <Button
                label="notifs"
                onClick={() => {
                      this.getNotifList();
                    }}>
                NO CLICK ME
                </Button>
                {this.renderObject()}
                
                {/* Modal to create new calendar */}
                <Dialog open={this.props.createPopUp} onClose={this.props.handleClose}>
                    <IconButton aria-label="close" className={classes.closeButton} onClick={this.props.handleClose}>
                        <CloseIcon />
                    </IconButton>
                    <DialogTitle id="customized-dialog-title" onClose={this.props.handleClose}>
                        Create a new calendar
                    </DialogTitle>
                    <DialogContent>
                        <TextField 
                          placeholder="Calendar Name"
                          margin="dense"
                          onChange={e => {
                            this.props.setCalName(e.target.value);
                          }}
                        />
                        <CirclePicker 
                          color={ this.props.colour }
                          onChangeComplete={ this.props.setCalColour }
                        />
                        <Button
                          label="Create Contact"
                          variant="contained" 
                          color="primary"
                          onClick={() => {
                            this.props.setNewCalendar(), this.props.handleClose();
                          }}
                        >
                        Create Calendar
                        </Button>
                    </DialogContent>
                </Dialog>
            </Drawer>
        );
    }
}

export default withStyles(styles)(Sidebar);
