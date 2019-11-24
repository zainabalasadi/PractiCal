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
    textBox: {
        marginBottom: 30,
        width: '100%',
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
        this.deleteCal = this.deleteCal.bind(this);
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

    deleteCal() {
        this.props.handleClose()
        let calendar = {"name": this.props.calName, "colour": this.props.calColour}
        let updatedCalendars = this.props.calendars.filter (
            cal => cal["name"] !== calendar.name
        );
        let deletedCalendar = this.props.calendars.filter (
            cal => cal["name"] === calendar.name
        );
        this.props.delete_calendar(deletedCalendar[0])
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
                            <ListItem className={classes.listItem} key={item.name} dense>
                                <div style={{backgroundColor: `${item.colour}`}} className={classes.colourPreview}></div>
                                <ListItemText id={labelId} primary={`${item.name}`} />
                                    <ListItemSecondaryAction>
                                        <IconButton edge="end" aria-label="comments" onClick={(e) => { this.props.handleClick(e, `${item.name}`, `${item.colour}`)} }>
                                            <MoreVertIcon className="threeDots"/>
                                        </IconButton>
                                    </ListItemSecondaryAction>
                                </ListItem>
                                {/* Menu for each calendar */}
                                <Menu
                                anchorEl={this.props.anchorEl}
                                keepMounted
                                open={Boolean(this.props.anchorEl)}
                                onClose={this.props.handleClose}>
                                <MenuItem onClick={this.props.handleCreateEdit}>Edit</MenuItem>
                                <MenuItem onClick={this.deleteCal}>Delete</MenuItem>
                            </Menu>
                        </div>         
                    );
                    })}
                    </List>

                {/* Modal to CREATE new calendar */}
                <Dialog maxWidth = {'xs'} open={this.props.createPopUp} onClose={this.props.handleClose}>
                    <IconButton aria-label="close" className={classes.closeButton} onClick={this.props.handleClose}>
                        <CloseIcon />
                    </IconButton>
                    <DialogTitle className={this.title} id="customized-dialog-title" onClose={this.props.handleClose}>
                        Create a new calendar
                    </DialogTitle>
                    <DialogContent>
                        <TextField
                          className={classes.textBox}
                          placeholder="Calendar name"
                          margin="dense"
                          onChange={e => {
                            this.props.setCalName(e.target.value);
                          }}/>
                        <h3>Select a calendar colour</h3><br/>
                        <CirclePicker
                          className={classes.colourPicker}
                          color={ this.props.colour }
                          onChangeComplete={ this.props.setCalColour }/><br/>
                    </DialogContent>
                    <DialogActions>
                        <Button
                          label="Create Calendar"
                          variant="contained"
                          color="primary"
                          onClick={() => {
                            this.props.setNewCalendar(), this.props.handleClose();
                          }}>
                        Create Calendar
                        </Button>
                    </DialogActions>
                </Dialog>

                {/* Modal to EDIT calendar */}
                <Dialog maxWidth = {'xs'} open={this.props.editPopUp} onClose={this.props.handleClose}>
                    <IconButton aria-label="close" className={classes.closeButton} onClick={this.props.handleClose}>
                        <CloseIcon />
                    </IconButton>
                    <DialogTitle className={this.title} id="customized-dialog-title" onClose={this.props.handleClose}>
                        Edit calendar
                    </DialogTitle>
                    <DialogContent>
                        <TextField
                          className={classes.textBox}
                          defaultValue={this.props.calName}
                          margin="dense"
                          onChange={e => {
                            this.props.setCalName(e.target.value);
                          }}/>
                        <h3>Select a calendar colour</h3><br/>
                        <CirclePicker
                          className={classes.colourPicker}
                          color={ this.props.calColour }
                          onChangeComplete={ this.props.setCalColour }/><br/>
                    </DialogContent>
                    <DialogActions>
                        <Button
                          label="Create Calendar"
                          variant="contained"
                          color="primary"
                          onClick={() => {
                            this.props.setEditCalendar(), this.props.handleClose();
                          }}>
                        Edit Calendar
                        </Button>
                    </DialogActions>
                </Dialog>
            </Drawer>
        );
    }
}

export default withStyles(styles)(Sidebar);
