import React, { Component } from "react";
import { Calendar, momentLocalizer} from 'react-big-calendar';
import { Dialog, DialogActions, DialogContent, Button, TextField } from "@material-ui/core";
import { InputLabel, Select, CssBaseline } from '@material-ui/core/';
import CloseIcon from '@material-ui/icons/Close';
import GroupIcon from '@material-ui/icons/Group';
import CalendarTodayIcon from '@material-ui/icons/CalendarToday';
import CategoryIcon from '@material-ui/icons/Category';
import ScheduleIcon from '@material-ui/icons/Schedule';
import NotesIcon from '@material-ui/icons/Notes';


import IconButton from '@material-ui/core/IconButton';
import moment from "moment";
import Navbar from './Navbar'
import Sidebar from './Sidebar'

import "!style-loader!css-loader!react-big-calendar/lib/css/react-big-calendar.css";
import { withStyles } from "@material-ui/core/styles";


// Initialise time localiser
const localizer = momentLocalizer(moment)

const drawerWidth = 300;
const navHeight = 64;

const styles = theme => ({
    calendar: {
        height: `calc(100% - ${navHeight}px - 43px)`, 
        position: "fixed", 
        width: `calc(100% - ${drawerWidth}px + 1px)`,
        marginLeft: "15px"
    },
    root: {
        display: 'flex',
    },
    appBar: {
        zIndex: theme.zIndex.drawer + 1,
    },
    drawer: {
        width: drawerWidth,
        flexShrink: 0,
    },
    drawerPaper: {
        width: drawerWidth,
        padding: theme.spacing(3),
    },
    content: {
        flexGrow: 1,
    },
    toolbar: theme.mixins.toolbar,
    title: {
        fontSize: 100,
        margin: '40px 0 20px 50px',
        maxWidth: 500,
        width: 500,
    },
    inputMargin: {
        margin: '4px 0 5px 0',
        marginLeft: 50,
        maxWidth: 500,
        width: 500,
        borderRadius: theme.shape.borderRadius,
        borderWidth: '50',
        '&:hover': {
            backgroundColor: '#F2F3F4',
        },
    },
    selectMargin: {
        margin: '4px 0 4px 0',
        marginLeft: 50,
        maxWidth: 150,
        width: 150,
    },
    closeButton: {
        position: 'absolute',
        right: theme.spacing(1),
        top: theme.spacing(1),
    },
    iconDiv: {
        position: 'relative', 
        display: 'inline-block'
    },
    icon: {
        position: 'absolute', 
        left: 4, 
        top: 10, 
        width: 20, height: 20,
        marginRight: 50,
    }
});


// Load events
class Cal extends Component {  
    constructor() {
        super();
        this.state = {
            events: [],
            calendars: [],
            title: "", start: "", end: "", desc: "",
            invitees: "", groups: "", calendar: "",
            eventId: "", category: "",
            openSlot: false,
            openEvent: false,
            clickedEvent: {},
        };
        this.handleClose = this.handleClose.bind(this);
    };

    componentDidMount() {
        this.get_calendars()
    }

    // Function to create event and send to back-end
    create_event(event) {
        //console.log(event)
        // console.log(event.state)
        console.log(JSON.stringify({"name": event.title, "desc": event.desc, 
                                    "startDate": event.start, "endDate": event.end, "invitees": event.invitees,
                                    "groups": event.groups, "calendar": event.calendar, "eventId": event.eventId}))
        let response = fetch('/createEvent', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
        body: JSON.stringify({"name": event.title, "desc": event.desc, 
                            "startDate": event.start, "endDate": event.end, "invitees": event.invitees,
                            "groups": event.groups, "calendar": event.calendar, "eventId": event.eventId})
        }).then((data) => data.json()).then(event => {
            console.log(event.success);
            if (event.success) {
                // append to events list
                console.log("Created event successfully")
                // event.start = new Date(event.start)
                // console.log(event.start)
                // event.end = new Date(event.end)
                // this.state.events.push(event)
            } else {
                console.log("Failed event creation")
            }
        });
    }

    // Function to edit event in back-end
    edit_event(event) {
        console.log(JSON.stringify({"name": event.title, "desc": event.desc, 
                                    "startDate": event.start, "endDate": event.end, "invitees": event.invitees,
                                    "groups": event.groups, "calendar": event.calendar, "eventId": event.eventId}))
        let response = fetch('/editEvent', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
        body: JSON.stringify({"name": event.title, "desc": event.desc, 
                            "startDate": event.start, "endDate": event.end, "invitees": event.invitees,
                            "groups": event.groups, "calendar": event.calendar, "eventId": event.eventId})
        }).then((data) => data.json());
    }

    delete_event(event) {
        console.log(JSON.stringify({"name": event.title, "desc": event.desc,
                                    "startDate": event.start, "endDate": event.end, "invitees": event.invitees,
                                    "groups": event.groups, "calendar": event.calendar, "eventId": event.eventId}))
        let response = fetch('/deleteEvent', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
        body: JSON.stringify({"name": event.title, "desc": event.desc,
                            "startDate": event.start, "endDate": event.end, "invitees": event.invitees,
                            "groups": event.groups, "calendar": event.calendar, "eventId": event.eventId})
        }).then((data) => data.json());
    }

    get_calendars() {
        let response = fetch('/getEvents', {
            method: 'GET'

        }).then((data) => data.json()).then(data => this.renderComponentsFromList(data));
    }

    renderComponentsFromList(calendarList) {
        for (var i = 0 ; i < calendarList.calendars.length ; i++) {
            this.state.calendars.push(calendarList.calendars[i])
            for (var j = 0 ; j < calendarList.calendars[i].events.length; j++) {
                //var startStr = JSON.parse(calendarList.calendars[i].events[j].start)
                console.log(calendarList.calendars[i].events[j].start)
                var start = new Date(calendarList.calendars[i].events[j].start)
                calendarList.calendars[i].events[j].start = start

                var end = new Date(calendarList.calendars[i].events[j].end)
                calendarList.calendars[i].events[j].end = end
                console.log(calendarList.calendars[i].events[j].start)

                this.state.events.push(calendarList.calendars[i].events[j])
            }
        }
        this.forceUpdate()
    }

    // Closes modal
    handleClose() {
        this.setState({ openEvent: false, openSlot: false });
    }

    formatDateStart(date) {
        
        var today = new Date();

        var d = new Date(date),
            month = '' + (d.getMonth() + 1),
            day = '' + d.getDate(),
            year = d.getFullYear(),
            hour = '' + today.getHours(),
            min = '' + today.getMinutes();
        
        // console.log(d)
    
        if (month.length < 2) 
            month = '0' + month;
        if (day.length < 2) 
            day = '0' + day;
        if (hour.length < 2) 
            hour = '0' + hour;
        if (min.length < 2) 
            min = '0' + min;
    
        return [year, month, day].join('-') + "T" + hour + ":" + '00';
    }

    formatDateEnd(date) {
        // console.log(date)
        var today = new Date();

        var d = new Date(date),
            month = '' + (d.getMonth() + 1),
            day = '' + d.getDate(),
            year = d.getFullYear(),
            hour = '' + (today.getHours() + 1),
            min = '' + today.getMinutes();
        
        // console.log(d)
    
        if (month.length < 2) 
            month = '0' + month;
        if (day.length < 2) 
            day = '0' + day;
        if (hour.length < 2) 
            hour = '0' + hour;
        if (min.length < 2) 
            min = '0' + min;
    
        return [year, month, day].join('-') + "T" + hour + ":" + '00';
    }

    formatActualDate(date) {
        var d = new Date(date),
            month = '' + (d.getMonth() + 1),
            day = '' + d.getDate(),
            year = d.getFullYear(),
            hour = '' + d.getHours(),
            min = '' + d.getMinutes();
        
        // console.log(d)
    
        if (month.length < 2) 
            month = '0' + month;
        if (day.length < 2) 
            day = '0' + day;
        if (hour.length < 2) 
            hour = '0' + hour;
        if (min.length < 2) 
            min = '0' + min;
    
        return [year, month, day].join('-') + "T" + hour + ":" + min;
    }
        
    //  Allows user to click on calendar slot and make new event
    handleSlotSelected(eventToEdit) {
        // console.log(eventToEdit.start);
        this.setState ({
            openSlot: true,
            title: eventToEdit.title,
            desc: eventToEdit.desc,
            start: eventToEdit.start,
            end: eventToEdit.end,
            invitees: eventToEdit.invitees,
            groups: eventToEdit.groups,
            calendar: eventToEdit.calendar,
            eventId: eventToEdit.eventId,
        });
    }
        
    //  Allows user to click on existing event
    handleEventSelected(event) {
        // console.log("event", event);
        this.setState ({
            openEvent: true,
            clickedEvent: event,
            start: event.start,
            end: event.end,
            title: event.title,
            desc: event.desc,
            invitees: event.invitees,
            groups: event.groups,
            calendar: event.calendar,
            eventId: event.eventId,
        });
    }
        
    // Sets the state of events
    setTitle(e) { this.setState({ title: e }); }
    setDescription(e) { this.setState({ desc: e }); }
    setInvitees(e) { this.setState({ invitees: e }); }
    setGroups(e) { this.setState({ groups: e }); }
    setCalendar(e) { this.setState({ calendar: e }); }
    setStart(e) { this.setState({ start: e }); }
    setEnd(e) { this.setState({ end: e }); }
    setCategory(e) { this.setState({ category: e }); }
        
    // Handle's start time select
    handleStartTime = (event, date) => {
        this.setState({ start: date });
    };
     
    // Handle's end time select
    handleEndTime = (event, date) => {
        this.setState({ end: date });
    };
        
    // Onclick callback function that pushes new event into events array.
    setNewEvent() {
        const { title, desc, start, end, invitees, groups, calendar, eventId, category } = this.state;
        let event = { title, desc, start, end, invitees, groups, calendar, eventId, category };
        let events = this.state.events.slice();

        var s = new Date(start)
        console.log(s)
        var e = new Date(end)
        console.log(e)

        let eventFE = { 
            "title": title,
            "desc": desc,
            "start": s,
            "end": e,
            "invitees": invitees,
            "groups": groups,
            "calendar": calendar,
            "eventId": eventId,
            "category": category,
        };

        events.push(eventFE);
        this.setState({ events });
        this.create_event(event)
    }
        
    // Updates Existing Event Title and/or Description
    updateEvent() {
        const { title, desc, start, end, events, invitees, groups, calendar, 
                clickedEvent, eventId, category } = this.state;
        const index = events.findIndex(event => event === clickedEvent);
        const updatedEvent = events.slice();
        updatedEvent[index].title = title;
        updatedEvent[index].desc = desc;
        updatedEvent[index].start = start;
        updatedEvent[index].end = end;
        updatedEvent[index].invitees = invitees;
        updatedEvent[index].groups = groups;
        updatedEvent[index].calendar = calendar;
        updatedEvent[index].eventId = eventId;
        updatedEvent[index].category = category;
        this.setState({
            events: updatedEvent
        });
        this.edit_event(updatedEvent[index])
    }
        
    // Filters out specific event that is to be deleted and set that variable to state
    deleteEvent() {
        let updatedEvents = this.state.events.filter (
            event => event["eventId"] !== this.state.eventId
        );

        let deletedEvent = this.state.events.filter (
            event => event["eventId"] === this.state.eventId
        )
        //console.log(updatedEvents)
        //console.log(deletedEvent)
        this.setState({ events: updatedEvents });
        this.delete_event(deletedEvent[0])
    }

    render() {
        const { classes } = this.props;
        return (
            <div className={classes.root} >
            <CssBaseline />
            <Navbar/>
            <main className={classes.content}>
                <div className={classes.toolbar} />
                <Calendar className={classes.calendar}
                //onLoad={console.log('LOADED')}
                  selectable
                  popup
                  localizer = {localizer}
                  defaultDate = {new Date()}
                  defaultView = "month"
                  events = {this.state.events}
                  showMultiDayTimes = {true}
                  onSelectSlot = {slotInfo => this.handleSlotSelected(slotInfo)}
                  onSelectEvent = {event => this.handleEventSelected(event)}
                //   components={{
                //     event: Event
                //   }}
                />
                {/* Modal for booking new event */}
                <Dialog contentStyle={{width: "100%", maxWidth: "none"}} open={this.state.openSlot} onClose={this.handleClose}>
                <IconButton aria-label="close" className={classes.closeButton} onClick={this.handleClose}>
                    <CloseIcon />
                </IconButton>
                  <DialogContent>
                    <TextField className={classes.title}
                    inputProps={{
                        style: {fontSize: 23} 
                    }}
                    placeholder="Add title"
                    fullWidth
                    autoFocus
                    margin="dense"
                    onChange={e => {
                      this.setTitle(e.target.value);
                    }}
                    />
                    <div className={classes.iconDiv}>
                        <ScheduleIcon className={classes.icon}/>
                        <TextField 
                          className={classes.inputMargin}
                          InputProps={{disableUnderline: true}}
                          type="datetime-local"
                          defaultValue={this.formatDateStart(this.state.start)}
                          onChange={e => {
                            this.setStart(e.target.value), this.handleStartTime;
                          }}
                        />
                        <TextField 
                          className={classes.inputMargin}
                          type="datetime-local"
                          defaultValue={this.formatDateEnd(this.state.end)}
                          InputProps={{disableUnderline: true}}
                          onChange={e => {
                            this.setEnd(e.target.value), this.handleEndTime;
                          }}
                        />
                    </div>
                    <div className={classes.iconDiv}>
                        <NotesIcon className={classes.icon}/>
                        <TextField 
                          className={classes.inputMargin}
                          fullWidth
                          placeholder="Add description"
                          margin="dense"
                          InputProps={{disableUnderline: true}}
                          onChange={e => {
                            this.setDescription(e.target.value);
                          }}
                        />
                    </div>
                    

                    <div className={classes.iconDiv}>
                        <GroupIcon className={classes.icon}/>
                        <TextField 
                          className={classes.inputMargin}
                          placeholder="Add invitees"
                          margin="dense"
                          InputProps={{disableUnderline: true}}
                          onChange={e => {
                            this.setInvitees(e.target.value);
                          }}
                        />

                        <TextField 
                          className={classes.inputMargin}
                          placeholder="Add group invitees"
                          margin="dense"
                          InputProps={{disableUnderline: true}}
                          onChange={e => {
                            this.setGroups(e.target.value);
                          }}
                        /> 
                    </div>
                    <div className={classes.iconDiv}>
                        <CalendarTodayIcon className={classes.icon}/>
                        <Select
                          native
                          InputProps={{disableUnderline: true}}
                          className={classes.selectMargin}
                          defaultValue='Default'
                          onChange={e => {
                            this.setCalendar(e.target.value);
                          }}
                        >
                        {this.state.calendars.map(item => {
                            return (
                                <option value={`${item.name}`}>{`${item.name}`}</option>
                            );
                        })}
                        </Select> 
                    </div><br />
                    <div className={classes.iconDiv}>
                        <CategoryIcon className={classes.icon}/>
                        <Select
                          native
                          defaultValue={this.state.category}
                          InputProps={{disableUnderline: true}}
                          className={classes.selectMargin}
                          defaultValue='Social'
                          onChange={e => {
                            this.setCategory(e.target.value);
                          }}
                        >
                        <option value="Work">Work</option>
                        <option value="Social">Social</option>
                        <option value="School">School</option>
                        <option value="Family">Family</option>
                        
                        </Select> 
                    </div>                 
                  </DialogContent>
                  <DialogActions>
                    <Button
                    label="Submit"
                    variant="contained" 
                    color="primary"
                    onClick={() => {
                        if (this.state.start >= this.state.end) {
                            
                            // console.log("i am hereeee")
                            // console.log(this.state.start)
                            // console.log(this.state.end)
                            this.handleClose();
                        } else {
                            this.setNewEvent(), this.handleClose();
                        }
                    }}
                    >
                    Submit
                    </Button>
                  </DialogActions>
                </Dialog>

                {/* Material-ui Modal for Existing Event */}
                <Dialog contentStyle={{width: "100%", maxWidth: "none"}} open={this.state.openEvent} onClose={this.handleClose}>
                <IconButton aria-label="close" className={classes.closeButton} onClick={this.handleClose}>
                    <CloseIcon />
                </IconButton>
                  <DialogContent>
                    <TextField 
                    className={classes.title}
                    inputProps={{
                        style: {fontSize: 23} 
                    }}
                    placeholder="Add title"
                    fullWidth
                    autoFocus
                    margin="dense"
                    defaultValue={this.state.title}
                    onChange={e => {
                      this.setTitle(e.target.value);
                    }}
                    />
                    <div className={classes.iconDiv}>
                        <ScheduleIcon className={classes.icon}/>
                        <TextField
                          className={classes.inputMargin}
                          InputProps={{disableUnderline: true}}
                          type="datetime-local"
                          defaultValue={this.formatActualDate(this.state.start)}
                          value={this.formatActualDate(this.state.start)}
                          onChange={e => {
                            this.setStart(e.target.value);
                          }}
                        />
                        <TextField
                          className={classes.inputMargin}
                          InputProps={{disableUnderline: true}}
                          type="datetime-local"
                          defaultValue={this.formatActualDate(this.state.start)}
                          value={this.formatActualDate(this.state.end)}
                          onChange={e => {
                            this.setEnd(e.target.value);
                          }}
                        />
                    </div>
                    <div className={classes.iconDiv}>
                        <NotesIcon className={classes.icon}/>
                        <TextField
                          className={classes.inputMargin}
                          fullWidth
                          placeholder="Add description"
                          InputProps={{disableUnderline: true}}
                          margin="dense"
                          multiline={true}
                          defaultValue={this.state.desc}
                          onChange={e => {
                            this.setDescription(e.target.value);
                          }}
                        />
                    </div>
                    <div className={classes.iconDiv}>
                        <GroupIcon className={classes.icon}/>
                        <TextField
                          className={classes.inputMargin}
                          defaultValue={this.state.invitees}
                          InputProps={{disableUnderline: true}}
                          placeholder="Add invitees"
                          margin="dense"
                          onChange={e => {
                            this.setInvitees(e.target.value);
                          }}
                        />

                        <TextField
                          className={classes.inputMargin}
                          defaultValue={this.state.group}
                          InputProps={{disableUnderline: true}}
                          placeholder="Add group invitees"
                          margin="dense"
                          onChange={e => {
                            this.setGroup(e.target.value);
                          }}
                        /> 
                    </div>
                    <div className={classes.iconDiv}>
                        <CalendarTodayIcon className={classes.icon}/>
                        <Select
                        native
                        value={this.state.calendar}
                        InputProps={{disableUnderline: true}}
                        className={classes.selectMargin}
                        defaultValue='Default'
                        onChange={e => {
                            this.setCalendar(e.target.value);
                        }}
                        >
                        {this.state.calendars.map(item => {
                            return (
                                <option value={`${item.name}`}>{`${item.name}`}</option>
                            );
                        })}
                        </Select> 
                    </div><br />
                    <div className={classes.iconDiv}>
                        <CategoryIcon className={classes.icon}/>
                        <Select
                          native
                          value={this.state.category}
                          InputProps={{disableUnderline: true}}
                          className={classes.selectMargin}
                          defaultValue='Social'
                          onChange={e => {
                            this.setCategory(e.target.value);
                          }}
                        >
                        <option value="Work">Work</option>
                        <option value="Social">Social</option>
                        <option value="School">School</option>
                        <option value="Family">Family</option>
                        
                        </Select> 
                    </div> 
                  </DialogContent>
                  <DialogActions>
                    <Button
                    label="Delete"
                    variant="contained" 
                    color="primary"
                    onClick={() => {
                      this.deleteEvent(), this.handleClose();
                    }}
                    >
                    Delete
                    </Button>
                    <Button
                    label="Edit"
                    variant="contained" 
                    color="primary"
                    onClick={() => {
                      this.updateEvent(), this.handleClose();
                    }}
                    >
                    Edit
                    </Button>
                  </DialogActions>
                </Dialog>
            </main>
            <Sidebar />
            </div>
        );
    }
}

function Event({ event }) {
    // let popoverClickRootClose = (
    //   <Popover id="popover-trigger-click-root-close" style={{ zIndex: 10000 }}>
    //     <strong>Holy guacamole!</strong> Check this info.
    //     <strong>{event.title}</strong>
    //   </Popover>
    // );
  
    // console.log(event);
    return (
      <div>
        <div>{event.start.getHours().toString()}</div>
        <div>{event.title}</div>
        
      </div>
    );
  }

export default withStyles(styles)(Cal);

// eventStyleGetter: function(event, start, end, isSelected) {
//     console.log(event);
//     var backgroundColor = '#' + event.hexColor;
//     var style = {
//         backgroundColor: backgroundColor,
//         borderRadius: '0px',
//         opacity: 0.8,
//         color: 'black',
//         border: '0px',
//         display: 'block'
//     };
//     return {
//         style: style
//     };
// },

// getEventStyle(event, start, end, isSelected) {
//     const style = {}
//     const todayDate = new Date().getDate()

//     if (start.getDate() === todayDate) {
//       style.backgroundColor = 'green'
//     } else if (start.getDate() < todayDate) {
//       style.backgroundColor = 'red'
//     } else if (start.getDate() > todayDate) {
//       style.backgroundColor = 'blue'
//     }
//     if (event.bgcolor) {
//       style.backgroundColor = event.bgcolor
//     }

//     return { style }
//   }


                  // UNCOMMENT LATER TO COLOUR DIFF EVENTS
                  //eventPropGetter={(this.eventStyleGetter)}
                //   eventPropGetter={event => ({
                //     style: {
                //       backgroundColor: event.color,
                //     },
                //   })}