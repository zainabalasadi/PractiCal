import React, { Component } from "react";
import { Calendar, momentLocalizer} from 'react-big-calendar';
import { Dialog, DialogActions, DialogContent, DialogTitle, DialogContentText, Button, TextField } from "@material-ui/core";
import { InputLabel, Select, CssBaseline } from '@material-ui/core/';
import CloseIcon from '@material-ui/icons/Close';
import GroupIcon from '@material-ui/icons/Group';
import CalendarTodayIcon from '@material-ui/icons/CalendarToday';
import CategoryIcon from '@material-ui/icons/Category';
import ScheduleIcon from '@material-ui/icons/Schedule';
import NotesIcon from '@material-ui/icons/Notes';
import NavigateBeforeIcon from '@material-ui/icons/NavigateBefore';
import NavigateNextIcon from '@material-ui/icons/NavigateNext';

import IconButton from '@material-ui/core/IconButton';
import moment from "moment";
import Navbar from './Navbar'
import Sidebar from './Sidebar'

import "!style-loader!css-loader!react-big-calendar/lib/css/react-big-calendar.css";
import { withStyles } from "@material-ui/core/styles"

// Initialise time localiser
const localizer = momentLocalizer(moment)

const drawerWidth = 300;
const navHeight = 75;

const styles = theme => ({
    calendar: {
        height: `calc(100% - ${navHeight}px - 40px)`,
        width: `calc(100% - ${drawerWidth}px + 1px)`,
        top: navHeight,
        position: "fixed",
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
    },
});


// Load events
class Cal extends Component {
    constructor() {
        super();
        this.state = {
            // Calendar
            events: [],
            calendars: [],
            title: "", start: "", end: "", desc: "",
            invitees: [], groups: [], calendar: "",
            eventId: "", category: "", colour: "",
            // Calendar Modals
            openSlot: false, openEvent: false, openNlp: false,
            clickedEvent: {},
            // Search
            searchResult: [], search: "", searchOpen: false,
            // NLP
	        nlpText: "", nlpResult: {}, notifs: [], anchorEl: null,
            createPopUp: false, editPopUp: false, calName: "", 
            calColour: "", oldCalName: "", oldCalColour: "",
        };
        this.handleClose = this.handleClose.bind(this);
        this.handleSearchClose = this.handleSearchClose.bind(this)
        this.get_calendars = this.get_calendars.bind(this)
        this.delete_calendar = this.delete_calendar.bind(this)
    };

    componentDidMount() {
        const view = this.props.view;
        this.get_calendars()
    }

    search = (keyword) => {
        console.log(keyword)
        this.setState({ searchResult: keyword, searchOpen: true })
        console.log(this.state.searchResult)
        renderSearchList(keyword)
    }

    renderSearchList(list) {
        return (
            <table className="searchTable">
            <tr>
                <th>Title</th>
                <th>Description</th>
                <th>Start Time</th>
                <th>End Time</th>
            </tr>
        { list.map((e) => {
                return (
                    <tr>
                        <td>{e.title}</td>
                        <td>{e.desc}</td>
                        <td>{new Date(e.start).getDate()}/{new Date(e.start).getMonth()}/{new Date(e.start).getFullYear()}  {new Date(e.start).getHours()}:{this.getMins(new Date(e.start).getMinutes())}</td>
                        <td>{new Date(e.end).getDate()}/{new Date(e.end).getMonth()}/{new Date(e.end).getFullYear()}  {new Date(e.end).getHours()}:{this.getMins(new Date(e.end).getMinutes())}</td>
                    </tr>
            )})}
            </table>
        )
    }

    getMins(mins) {
    var s = String(mins)
        if (s.length < 2) {
            return '0' + s
        } else {
            return s
        }
    }

    // Function to create event and send to back-end
    create_event(event) {
        //console.log(event)
        console.log(this.state)
        console.log(JSON.stringify({"name": event.title, "desc": event.desc,
                                    "startDate": this.formatActualDate(event.start), "endDate": this.formatActualDate(event.end), "invitees": event.invitees,
                                    "groups": event.groups, "calendar": event.calendar, "eventId": event.eventId,
                            "category": event.category}))
        let response = fetch('/createEvent', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
        body: JSON.stringify({"name": event.title, "desc": event.desc,
                            "startDate": this.formatActualDate(event.start), "endDate": this.formatActualDate(event.end), "invitees": event.invitees,
                            "groups": event.groups, "calendar": event.calendar, "eventId": event.eventId,
                            "category": event.category})}).then((data) => data.json()).then(event => {
            if (event.success) {
                // append to events list
                this.setState({ events: [], calendars: [] })
                this.get_calendars()
                console.log("Created event successfully")
            } else {
                console.log("Failed event creation")
            }
        });
    }

    // Function to edit event in back-end
    edit_event(event) {
        console.log(JSON.stringify({"name": event.title, "desc": event.desc,
                                    "startDate": event.start, "endDate": event.end, "invitees": event.invitees,
                                    "groups": event.groups, "calendar": event.calendar, "eventId": event.eventId,
                            "category": event.category}))
        let response = fetch('/editEvent', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
        body: JSON.stringify({"name": event.title, "desc": event.desc,
                            "startDate": event.start, "endDate": event.end, "invitees": event.invitees,
                            "groups": event.groups, "calendar": event.calendar, "eventId": event.eventId,
                            "category": event.category})}).then((data) => data.json()).then(data => this.forceUpdate());
    }

    delete_event(event) {
        // console.log(JSON.stringify({"name": event.title, "desc": event.desc,
        //                             "startDate": event.start, "endDate": event.end, "invitees": event.invitees,
        //                             "groups": event.groups, "calendar": event.calendar, "eventId": event.eventId,
        //                     "category": event.category}))
        let response = fetch('/deleteEvent', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
        body: JSON.stringify({"name": event.title, "desc": event.desc,
                            "startDate": event.start, "endDate": event.end, "invitees": event.invitees,
                            "groups": event.groups, "calendar": event.calendar, "eventId": event.eventId,
                            "category": event.category})}).then((data) => data.json());
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
                // Format start date
                var start = new Date(calendarList.calendars[i].events[j].start)
                calendarList.calendars[i].events[j].start = start
                // Format end date
                var end = new Date(calendarList.calendars[i].events[j].end)
                calendarList.calendars[i].events[j].end = end
                // Add colour as attribute
                calendarList.calendars[i].events[j].colour = calendarList.calendars[i].colour;
                this.state.events.push(calendarList.calendars[i].events[j])
            }
        }
        this.forceUpdate()
    }

    // Closes modal
    handleClose() {
        this.setState({ openEvent: false, openSlot: false, openNlp: false,
                        createPopUp: false, editPopUp: false, anchorEl: null });
    }

    handleSearchClose() {
        this.setState({ searchOpen: false })
    }

    formatDateStart(date) {
        var today = new Date();
        var d = new Date(date),
            month = '' + (d.getMonth() + 1),
            day = '' + d.getDate(),
            year = d.getFullYear(),
            hour = '' + d.getHours(),
            min = '' + d.getMinutes();


        if (month.length < 2)
            month = '0' + month;
        if (day.length < 2)
            day = '0' + day;
        if (hour.length < 2)
            hour = '0' + hour;
        if (min.length < 2)
            min = '0' + min

        return [year, month, day].join('-') + "T" + hour + ":" + min;
    }

    formatDateEnd(date) {
        var today = new Date();
        var d = new Date(date),
            month = '' + (d.getMonth() + 1),
            day = '' + d.getDate(),
            year = d.getFullYear(),
            hour = '' + (d.getHours()),
            min = '' + d.getMinutes();

        if (month.length < 2)
            month = '0' + month;
        if (day.length < 2)
            day = '0' + day;
        if (hour.length < 2)
            hour = '0' + hour;
        if (min.length < 2)
            min = '0' + min

        return [year, month, day].join('-') + "T" + hour + ":" + min;
    }

    formatActualDate(date) {
        var d = new Date(date),
            month = '' + (d.getMonth() + 1),
            day = '' + d.getDate(),
            year = d.getFullYear(),
            hour = '' + d.getHours(),
            min = '' + d.getMinutes();

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
            category: eventToEdit.category,
        });
    }

    //  Allows user to click on existing event
    handleEventSelected(event) {
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
            category: event.category,
        });
    }

    // Sets the state of events
    setTitle(e) { this.setState({ title: e }); }
    setDescription(e) { this.setState({ desc: e }); }
    setInvitees(e) { this.setState({ invitees: e }); }
    setGroups(e) { this.setState({ groups: e }); }
    setCalendar(e) { this.setState({ calendar: e }), this.setState({ colour: e.colour }); }
    setStart(e) { this.setState({ start: e }); }
    setEnd(e) { this.setState({ end: e }); }
    setCategory(e) { this.setState({ category: e }); }

    handleNlpTextbox = (val) => { this.setState({ nlpText: val }); };

    handleNlpData = (e) => {
        var d = new Date(),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear(),
        hour = '' + d.getHours(),
        min = '' + d.getMinutes();

        if (month.length < 2)
            month = '0' + month;
        if (day.length < 2)
            day = '0' + day;
        if (hour.length < 2)
            hour = '0' + hour;
        if (min.length < 2)
            min = '0' + min;
	    	if (e.date == "") {
		    e.date = [year, month, day].join('-') + "T"
		}
		if (e.timeStart == "") {
        	e.timeStart=[year, month, day].join('-') + "T" + hour + ":" + '00';
		}
		if (e.timeEnd == "") {
			e.timeEnd = e.timeStart
		}
		this.setState({title: e.eventName, desc: "", start: e.date.substring(0, 10).concat(e.timeStart.substring(10, 16)), end: e.date.substring(0, 10).concat(e.timeEnd.substring(10, 16)), invitees: "", groups: "", openNlp: true})
		console.log(this.state)
    }

    handleCreateOpen = () => {
        this.setState ({ createPopUp: true });
    };

    handleCreateEdit = (name) => {
        this.setState ({ editPopUp: true });
    };

    setEditCalendar = () => {
        const { name, colour } = this.state;
        if (!name) {
            const name = this.state.oldCalName
            let cal = { name, colour };
            this.edit_calendar(cal, this.state.oldCalName)
            this.handleClose
        } else if (!colour) {
            const colour = this.state.oldCalColour
            let cal = { name, colour };
            this.edit_calendar(cal, this.state.oldCalName)
            this.handleClose
        } else if (name && colour) {
            let cal = { name, colour };
            this.edit_calendar(cal, this.state.oldCalName)
        }
    }

    handleDeleteCal = (calendarName) => {
        var string = 'deleting' + calendarName
        console.log(string)
    }

    setCalName = (e) => {
        this.setState({ name: e });
    };

    setCalColour = (e) => {
        this.setState({ colour: e.hex });
    };

    setNewCalendar = () => {
        const { name, colour } = this.state;
        let newCal = { name, colour };
        let calendars = this.state.calendars.slice();
        calendars.push(newCal);
        this.setState({ calendars });
        this.create_calendar(newCal)
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
                //this.state.calendars.push(calendar)
            } else {
                console.log("Failed calendar creation")
            }
        });
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
                console.log("Suceeededdddd")
                this.setState({events: [], calendars: []})
                this.get_calendars()
            } else {
                console.log("Failedddddddd")
            }
        });
    }

    edit_calendar(calendar, oldName) {
        let response = fetch('/editCalendar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
        body: JSON.stringify({"oldName": oldName, "name": calendar.name, "colour": calendar.colour})
        }).then((data) => data.json()).then(data => {
            if (data.success) {
                this.setState({events: [], calendars: []})
                this.get_calendars()
            } else {
                console.log("Failed")
            }
        });
    }

    handleClick = (e, name, colour) => {
        this.setState({ anchorEl: e.currentTarget, calName: name, calColour: colour,
                        oldCalName: name, oldCalColour: colour, });
  	};

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

         console.log("for FE")
        var s = new Date(start)
        console.log(s)
        var e = new Date(end)
        console.log(e)
        console.log("for BE")
        console.log(start)
        console.log(end)


        console.log("HELLO WORLD")

        updatedEvent[index].title = title;
        updatedEvent[index].desc = desc;
        updatedEvent[index].start = s;
        updatedEvent[index].end = e;
        updatedEvent[index].invitees = invitees;
        updatedEvent[index].groups = groups;
        updatedEvent[index].calendar = calendar;
        updatedEvent[index].eventId = eventId;
        updatedEvent[index].category = category;

        let eventBE = {
            "title": title,
            "desc": desc,
            "start": start,
            "end": end,
            "invitees": invitees,
            "groups": groups,
            "calendar": calendar,
            "eventId": eventId,
            "category": category,
        };

        this.setState({ events: updatedEvent });
        this.forceUpdate()
        this.edit_event(eventBE)
    }

    // Filters out specific event that is to be deleted and set that variable to state
    deleteEvent() {
        let updatedEvents = this.state.events.filter (
            event => event["eventId"] !== this.state.eventId
        );

        let deletedEvent = this.state.events.filter (
            event => event["eventId"] === this.state.eventId
        )
        this.setState({ events: updatedEvents });
        this.delete_event(deletedEvent[0])
    }

    eventStyleGetter(event) {
        var backgroundColor = event.colour;
        var style = {
            backgroundColor: backgroundColor,
        };
        return {
            style: style
        };
    }

    render() {
        const { classes } = this.props;
        return (
            <div className={classes.root} >
            <CssBaseline />
            <Navbar func={this.search}/>
            <main className={classes.content}>
                <div className={classes.toolbar} />
                <Calendar className={classes.calendar}
                  selectable
                  popup
                  localizer = {localizer}
                  defaultDate = {new Date()}
                  {...this.props}
                  defaultView = "month"
                  events = {this.state.events}
                  components={{
                    event: Event,
                    toolbar: CustomToolbar,
                  }}
                  showMultiDayTimes = {true}
                  onSelectSlot = {slotInfo => this.handleSlotSelected(slotInfo)}
                  onSelectEvent = {event => this.handleEventSelected(event)}
                  eventPropGetter={(this.eventStyleGetter)}
                />
                {/* Modal for booking new event */}
                <Dialog contentstyle={{width: "100%", maxWidth: "none"}} open={this.state.openSlot} onClose={this.handleClose} onEntered={this.handleOpenDialog}>
                <IconButton aria-label="close" className={classes.closeButton} onClick={this.handleClose}>
                    <CloseIcon />
                </IconButton>
                  <DialogContent>
                    <TextField
                    className={classes.title}
                    inputProps={{ style: {fontSize: 23} }}
                    placeholder="Add title"
                    autoFocus
                    margin="dense"
                    onChange={e => {
                      this.setTitle(e.target.value);
                    }}/>
                    <div className={classes.iconDiv}>
                        <ScheduleIcon className={classes.icon}/>
                        <TextField
                          className={classes.inputMargin}
                          InputProps={{disableUnderline: true}}
                          type="datetime-local"
                          defaultValue={this.formatDateStart(this.state.start)}
                          //value = {this.formatDateStart(this.state.start)}
                          onChange={e => {
                            this.setStart(e.target.value), this.handleStartTime;
                          }}/>
                        <TextField
                          className={classes.inputMargin}
                          type="datetime-local"
                          defaultValue={this.formatDateEnd(this.state.end)}
                          //value = {new Date(this.formatDateEnd(this.state.end))}
                          InputProps={{disableUnderline: true}}
                          onChange={e => {
                            this.setEnd(e.target.value), this.handleEndTime;
                          }}/>
                    </div>
                    <div className={classes.iconDiv}>
                        <NotesIcon className={classes.icon}/>
                        <TextField
                          className={classes.inputMargin}
                          placeholder="Add description"
                          margin="dense"
                          InputProps={{disableUnderline: true}}
                          onChange={e => {
                            this.setDescription(e.target.value);
                          }}/>
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
                          }}/>
                        <TextField
                          className={classes.inputMargin}
                          placeholder="Add group invitees"
                          margin="dense"
                          InputProps={{disableUnderline: true}}
                          onChange={e => {
                            this.setGroups(e.target.value);
                          }}/>
                    </div>
                    <div className={classes.iconDiv}>
                        <CalendarTodayIcon className={classes.icon}/>
                        <Select
                          native
                          className={classes.selectMargin}
                          defaultValue='Select Calendar'
                          onChange={e => {
                            this.setCalendar(e.target.value), this.eventStyleGetter(this.state);
                          }}>
                        <option value="">Select Calendar</option>
                        {
                            this.state.calendars.map(item => {
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
                          className={classes.selectMargin}
                          defaultValue='Select Category'
                          onChange={e => {
                            this.setCategory(e.target.value);
                          }}>
                        <option value="">Select Category</option>
                        <option value="Work">Work</option>
                        <option value="Social">Social</option>
                        <option value="School">School</option>
                        <option value="Family">Family</option>
                        <option value="Miscellaneous">Miscellaneous</option>
                        </Select>
                    </div>
                  </DialogContent>
                  <DialogActions>
                    <Button
                    label="Submit"
                    variant="contained"
                    color="primary"
                    onClick={() => {
                        console.log(this.state.start)
                        console.log(this.state.end)
                        if (this.state.title == null) {
                            alert("Please provide a title.")
                        } else if (this.state.start >= this.state.end) {
                            alert("Please enter valid dates.")
                        } else if (this.state.calendar == null) {
                            alert("Please select a calendar.")
                        } else {
                            this.setNewEvent(), this.handleClose();
                        }
                    }}>
                    Submit
                    </Button>
                  </DialogActions>
                </Dialog>

                {/* Material-ui Modal for Existing Event */}
                <Dialog contentstyle={{width: "100%", maxWidth: "none"}} open={this.state.openEvent} onClose={this.handleClose}>
                <IconButton aria-label="close" className={classes.closeButton} onClick={this.handleClose}>
                    <CloseIcon />
                </IconButton>
                  <DialogContent>
                    <TextField
                    className={classes.title}
                    inputProps={{ style: {fontSize: 23} }}
                    placeholder="Add title"
                    autoFocus
                    margin="dense"
                    value={this.state.title}
                    onChange={e => {
                      this.setTitle(e.target.value);
                    }}/>
                    <div className={classes.iconDiv}>
                        <ScheduleIcon className={classes.icon}/>
                        <TextField
                          className={classes.inputMargin}
                          InputProps={{disableUnderline: true}}
                          type="datetime-local"
                          value={this.formatActualDate(this.state.start)}
                          onChange={e => {
                            this.setStart(e.target.value);
                          }}/>
                        <TextField
                          className={classes.inputMargin}
                          InputProps={{disableUnderline: true}}
                          type="datetime-local"
                          value={this.formatActualDate(this.state.end)}
                          onChange={e => {
                            this.setEnd(e.target.value);
                          }}/>
                    </div>
                    <div className={classes.iconDiv}>
                        <NotesIcon className={classes.icon}/>
                        <TextField
                          className={classes.inputMargin}
                          placeholder="Add description"
                          InputProps={{disableUnderline: true}}
                          margin="dense"
                          multiline={true}
                          value={this.state.desc}
                          onChange={e => {
                            this.setDescription(e.target.value);
                          }}/>
                    </div>
                    <div className={classes.iconDiv}>
                        <GroupIcon className={classes.icon}/>
                        <TextField
                          className={classes.inputMargin}
                          value={this.state.invitees}
                          InputProps={{disableUnderline: true}}
                          placeholder="Add invitees"
                          margin="dense"
                          onChange={e => {
                            this.setInvitees(e.target.value);
                          }}/>
                        <TextField
                          className={classes.inputMargin}
                          value={this.state.group}
                          InputProps={{disableUnderline: true}}
                          placeholder="Add group invitees"
                          margin="dense"
                          onChange={e => {
                            this.setGroup(e.target.value);
                          }}/>
                    </div>
                    <div className={classes.iconDiv}>
                        <CalendarTodayIcon className={classes.icon}/>
                        <Select
                        native
                        value={this.state.calendar}
                        className={classes.selectMargin}
                        onChange={e => {
                            this.setCalendar(e.target.value), this.eventStyleGetter();
                        }}>
                        <option value="">Select Calendar</option>
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
                          className={classes.selectMargin}
                          onChange={e => {
                            this.setCategory(e.target.value);
                          }}>
                        <option value="Work">Work</option>
                        <option value="Social">Social</option>
                        <option value="School">School</option>
                        <option value="Family">Family</option>
                        <option value="Miscellaneous">Miscellaneous</option>
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
                    }}>
                    Delete
                    </Button>
                    <Button
                    label="Edit"
                    variant="contained"
                    color="primary"
                    onClick={() => {
                        if (this.state.title == null) {
                            alert("Please provide a title.")
                        } else if (new Date(this.state.start) >= new Date(this.state.end)) {
                            alert("Please enter valid dates.")
                        } else if (this.state.calendar == null) {
                            alert("Please select a calendar.")
                        } else {
                            console.log(this.state.start)
                            console.log(this.state.end)
                            this.updateEvent(), this.handleClose();
                        }
                    }}>
                    Edit
                    </Button>
                  </DialogActions>
                </Dialog>

                <Dialog
                    maxWidth = {'md'}
                    open={this.state.searchOpen}
                    onClose={this.handleSearchClose}>
                        <IconButton aria-label="close" className={classes.closeButton} onClick={this.handleSearchClose}>
                            <CloseIcon />
                        </IconButton>
                        <DialogTitle>{`Search results`}</DialogTitle>
                        <DialogContent>
                            <DialogContentText>
                                {this.renderSearchList(this.state.searchResult)}
                            </DialogContentText>
                        </DialogContent>
                </Dialog>

		        {/* Material-ui Modal for nlp Event */}
                <Dialog contentstyle={{width: "100%", maxWidth: "none"}} open={this.state.openNlp} onClose={this.handleClose}>
                <IconButton aria-label="close" className={classes.closeButton} onClick={this.handleClose}>
                    <CloseIcon />
                </IconButton>
                  <DialogContent>
                    <TextField
                      className={classes.title}
                      inputProps={{ style: {fontSize: 23} }}
                      placeholder="Add title"
                      autoFocus
                      margin="dense"
                      value={this.state.title}
                      onChange={e => {
                        this.setTitle(e.target.value);
                    }}/>
                    <div className={classes.iconDiv}>
                        <ScheduleIcon className={classes.icon}/>
                        <TextField
                          className={classes.inputMargin}
                          InputProps={{ disableUnderline: true }}
                          type="datetime-local"
                        //   defaultValue={this.formatActualDate(this.state.start)}
                          value={this.formatActualDate(this.state.start)}
                          onChange={e => {
                            this.setStart(e.target.value);
                          }}/>
                        <TextField
                          className={classes.inputMargin}
                          InputProps={{disableUnderline: true}}
                          type="datetime-local"
                        //   defaultValue={this.formatActualDate(this.state.end)}
                          value={this.formatActualDate(this.state.end)}
                          onChange={e => {
                            this.setEnd(e.target.value);
                          }}/>
                    </div>
                    <div className={classes.iconDiv}>
                        <NotesIcon className={classes.icon}/>
                        <TextField
                          className={classes.inputMargin}
                          placeholder="Add description"
                          InputProps={{disableUnderline: true}}
                          margin="dense"
                          multiline={true}
                          value={this.state.desc}
                          onChange={e => {
                            this.setDescription(e.target.value);
                          }}/>
                    </div>
                    <div className={classes.iconDiv}>
                        <GroupIcon className={classes.icon}/>
                        <TextField
                          className={classes.inputMargin}
                          value={this.state.invitees}
                          InputProps={{disableUnderline: true}}
                          placeholder="Add invitees"
                          margin="dense"
                          onChange={e => {
                            this.setInvitees(e.target.value);
                          }}/>
                        <TextField
                          className={classes.inputMargin}
                          value={this.state.group}
                          InputProps={{disableUnderline: true}}
                          placeholder="Add group invitees"
                          margin="dense"
                          onChange={e => {
                            this.setGroup(e.target.value);
                          }}/>
                    </div>
                    <div className={classes.iconDiv}>
                        <CalendarTodayIcon className={classes.icon}/>
                        <Select
                          native
                          className={classes.selectMargin}
                          defaultValue='Select Calendar'
                          onChange={e => {
                            this.setCalendar(e.target.value), this.eventStyleGetter(this.state);
                          }}>
                        <option value="">Select Calendar</option>
                        {
                            this.state.calendars.map(item => {
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
                          className={classes.selectMargin}
                          defaultValue='Select Category'
                          onChange={e => {
                            this.setCategory(e.target.value);
                          }}>
                        <option value="">Select Category</option>
                        <option value="Work">Work</option>
                        <option value="Social">Social</option>
                        <option value="School">School</option>
                        <option value="Family">Family</option>
                        <option value="Miscellaneous">Miscellaneous</option>
                        </Select>
                    </div>
                  </DialogContent>
                  <DialogActions>
                    <Button
                    label="submit"
                    variant="contained"
                    color="primary"
                    onClick={() => {
                      this.setNewEvent(), this.handleClose();
                    }}>
                    Submit
                    </Button>
                  </DialogActions>
                </Dialog>

            </main>
            <Sidebar calendars={this.state.calendars} nlpText={this.state.nlpText}
                    handleNlpData={this.handleNlpData} notifs={this.state.notifs}
                    createPopUp={this.state.createPopUp} calName={this.state.calName}
                    calColour={this.state.calColour} anchorEl={this.state.anchorEl}
                    handleCreateOpen={this.handleCreateOpen} handleClose={this.handleClose}
                    handleDeleteCal={this.handleDeleteCal} setCalName={this.setCalName}
                    setCalColour={this.setCalColour} setNewCalendar={this.setNewCalendar}
                    handleClick={this.handleClick} setNlpBarState={this.handleNlpTextbox}
                    events={this.state.events} delete_calendar={this.delete_calendar}
                    handleCreateEdit={this.handleCreateEdit} editPopUp={this.state.editPopUp}
                    oldCalName={this.state.oldCalName} setEditCalendar={this.setEditCalendar}/>
            </div>
        );
    }
}

function Event({ event }) {
    var start = new Date(event.start),
        hour = start.getHours();
    var ampm = "am "

    if (hour > 12) {
        hour -= 12;
        ampm = "pm "
    } else if (hour === 0) {
       hour = 12;
    }

    return (
        <div>{hour}{ampm}{event.title}</div>
    );
  }

class CustomToolbar extends React.Component {
    render() {
        let { localizer: { messages }, label } = this.props
        const { classes } = this.props;
        return(
            <div className="rbc-toolbar">
                {/* Arrows */}
                <NavigateBeforeIcon className="prevNext" onClick={this.navigate.bind(null, navigate.PREVIOUS)}/>
                <p className="prevNext todayButton"onClick={this.navigate.bind(null, navigate.TODAY)}>Today</p>
                <NavigateNextIcon className="prevNext" onClick={this.navigate.bind(null, navigate.NEXT)}/>
                {/* Title */}
                <span className="rbc-toolbar-label">{label}</span>
                {/* Views */}
                <div className="rbc-btn-group">
					<button type="button" onClick={this.view.bind(null, 'month')}>Month</button>
					<button type="button" onClick={this.view.bind(null, 'week')}>Week</button>
					<button type="button" onClick={this.view.bind(null, 'day')}>Day</button>
					<button type="button" onClick={this.view.bind(null, 'agenda')}>Schedule</button>
				</div>
            </div>
        )
    }
    navigate = action => {
        this.props.onNavigate(action)
    }
    view = action => {
        this.props.onView(action);
    }
}

export let navigate = {
    PREVIOUS: 'PREV',
    NEXT: 'NEXT',
    TODAY: 'TODAY',
    DATE: 'DATE',
}

export default withStyles(styles)(Cal);
