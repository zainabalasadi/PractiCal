import React, { Component } from "react";
import { fade } from '@material-ui/core/styles';
import { AppBar, Toolbar, InputBase } from '@material-ui/core';
import { Dialog, DialogTitle, DialogContent, Button, TextField, Typography } from "@material-ui/core";
import IconButton from '@material-ui/core/IconButton';
import SearchIcon from '@material-ui/icons/Search';
import CloseIcon from '@material-ui/icons/Close';
import PeopleIcon from '@material-ui/icons/People';
import logo from '../../../public/logo.svg';
import { withStyles } from "@material-ui/core/styles";
import TimeBreakdown from './TimeBreakdown'
import Notification from './Notification'

const navHeight = 64;

const styles = theme => ({
    nav: {
        // zIndex: '1400',
        backgroundColor: theme.palette.common.white,
        color: fade(theme.palette.common.black, 0.7),
        height: navHeight,
    },

    grow: {
        flexGrow: 1,
    },
    menuButton: {
        marginRight: theme.spacing(2),
    },

    title: {
        width: '100px',
        [theme.breakpoints.up('sm')]: {
            display: 'block',
        },
    },

    search: {
        position: 'relative',
        borderRadius: theme.shape.borderRadius,
        borderWidth: '10',
        backgroundColor: '#F2F3F4',
        '&:hover': {
            backgroundColor: fade('#F2F3F4', 0.8),
        },
        marginRight: theme.spacing(2),
        marginLeft: 0,
        width: '100%',
        [theme.breakpoints.up('sm')]: {
            marginLeft: theme.spacing(3),
        width: 'auto',
        },
    },

    searchIcon: {
        width: theme.spacing(7),
        height: '100%',
        position: 'absolute',
        pointerEvents: 'none',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
    },

    inputRoot: {
        color: 'inherit',
    },

    inputInput: {
        padding: theme.spacing(1, 1, 1, 7),
        transition: theme.transitions.create('width'),
        width: '100%',
        [theme.breakpoints.up('md')]: {
            width: 200,
        },
    },

    root: {
        margin: 0,
        padding: theme.spacing(2),
    },

    closeButton: {
        position: 'absolute',
        right: theme.spacing(1),
        top: theme.spacing(1),
    },

});

class Navbar extends Component {
    constructor(props) {
        super(props);
        this.state = {
            contacts: [
                {
                  contactName: 'Jeff Lastname',
                  contactEmail: 'jeff@email.com',
                },
            ],
            groups: [
                {
                  groupName: 'COMP4920',
                  groupEmail: 'jeff@email.com;sarah@email.com;alice@email.com',
                },
            ],
            notifs: [

            ],
            groupName: "",
            groupEmail: "",
            contactName: "",
            contactEmail: "",
            openContacts: false,
            openNotification: false,
            searchText: "",
        };
        this.handleClose = this.handleClose.bind(this);
        this.handleContactOpen = this.handleContactOpen.bind(this);
    };

    setSearchText(e) {
        this.setState({ searchText: e.target.value })
    }

    search() {
        let response = fetch('/searchEvents', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
        body: JSON.stringify({"queryString": this.state.searchText})
        }).then(response => response.json()).then(data => this.showSearchResults(data))
        // }).then(response => response.json()).then(data => console.log(data))
        // TODO Insert code to change state of front end given response from the back end
    }

    showSearchResults(events) {
        console.log(events)
        for(var i = 0; i < events.length; i++) {
            //console.log(events[i].desc)
        }
        this.props.func(events)
    }

    // Function to create contact and send to back-end
    create_contact(contact) {
        console.log(contact)
        let response = fetch('/addContact', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
        body: JSON.stringify({"email": contact.contactName, "name": contact.ContactEmail})
        })
	

    }

    // Function to create group and send to back-end
    create_group(group) {
        //console.log(group)

    }

    setNewContact() {
        const { contactName, contactEmail } = this.state;
        let newContact = { contactName, contactEmail };
        let contacts = this.state.contacts.slice();
        contacts.push(newContact);
        this.setState({ contacts: contacts });
        this.create_contact(newContact)
    }

    setNewGroup() {
        const { groupName, groupEmail } = this.state;
        let newGroup = { groupName, groupEmail };
        let groups = this.state.groups.slice();
        groups.push(newGroup);
        this.setState({ groups: groups });
        this.create_group(newGroup)
    }

    // Sets the state of input
    setContactEmail(e) {
        this.setState({ contactEmail: e });
    };
    setContactName(e) {
        this.setState({ contactName: e });
    };
    setGroupEmail(e) {
        this.setState({ groupEmail: e });
    };
    setGroupName(e) {
        this.setState({ groupName: e });
    };

    handleContactOpen() {
        this.setState ({
            openContacts: true,
        });
    };

    handleClose() {
        this.setState({ openContacts: false, openNotification: false });
    };

//     get_notifs() {
//         let response = fetch('/getNotifs', {
//             method: 'GET'
//
//         }).then((data) => data.json()).then(data => this.renderComponentsFromList(data));
//     }
//
// //     NOW THAT ITS IN STATE HOW DO I PASS THIS ONTO <NOTIFICATION/>
//     renderComponentsFromList(notifList) {
//         //console.log(notifList)
//
//         var new_list = new Array()
//         for (var i = 0 ; i < notifList.length ; i++) {
//             console.log(notifList[i])
//             new_list.push(notifList[i])
//         }
//
//         this.setState((prevState) => {
//             events: Array.prototype.push.apply(prevState.notifs, new_list)
//         })
//     }

    logout() {
      let response = fetch('/logout', {
          method: 'GET',
      }).then((data) => data.json())
    }

    render() {
        const { classes } = this.props;
        return (
        <div className={classes.grow}>
            <AppBar position="fixed" elevation={0} className={classes.nav}>
                <Toolbar>
                    <img className={classes.title} src={logo} alt="logo" />
                    <div className={classes.search}>
                        <div className={classes.searchIcon}>
                            <SearchIcon />
                        </div>
                        <InputBase
                        fullWidth={true}
                        placeholder="Search"
                        classes={{
                            root: classes.inputRoot,
                            input: classes.inputInput,
                        }}
                        inputProps={{ 'aria-label': 'search' }}
                        name="search"
                        value={this.state.searchText}
                        onChange={e => {
                            this.setSearchText(e)
                        }}
                        onKeyPress={e => {
                            if (e.key === "Enter") {
                                this.search()
                                this.setState({ searchText: ""})
                            }
                        }}
                        />
                    </div>

                    <div className={classes.grow} />
                    <Notification /*data={this.get_notifs()}*//>
                    <TimeBreakdown/>
                    <div>
                        <IconButton color="inherit" onClick={this.handleContactOpen}>
                            <PeopleIcon />
                        </IconButton>
                            <a href="/">
                              <Button label="Logout" onClick={() => { this.logout(); }}>
                                LOGOUT
                              </Button>
                            </a>
                    </div>
                </Toolbar>
            </AppBar>

            {/* Modal for contacts */}
            <Dialog open={this.state.openContacts} onClose={this.handleClose}>
                <IconButton aria-label="close" className={classes.closeButton} onClick={this.handleClose}>
                    <CloseIcon />
                </IconButton>
                <DialogTitle id="customized-dialog-title" onClose={this.handleClose}>
                    My Contacts
                </DialogTitle>

                <DialogContent>
                    <TextField
                        placeholder="Group name"
                        margin="dense"
                        onChange={e => {this.setGroupName(e.target.value)}}
                    />
                    <TextField
                        placeholder="Emails"
                        margin="dense"
                        onChange={e => {this.setGroupEmail(e.target.value)}}
                    />
                    <Button
                        label="Create Group"
                        variant="contained"
                        color="primary"
                        onClick={() => {
                            this.setNewGroup();
                        }}
                        >
                        Create Group
                        </Button>



                        <TextField
                        placeholder="Contact name"
                        margin="dense"
                        onChange={e => {this.setContactName(e.target.value)}}
                    />
                    <TextField
                        placeholder="Email"
                        margin="dense"
                        onChange={e => {this.setContactEmail(e.target.value)}}
                    />
                    <Button
                        label="Create Contact"
                        variant="contained"
                        color="primary"
                        onClick={() => {
                            this.setNewContact();
                        }}
                        >
                        Create Contact
                        </Button>
                    <ul>
                    {this.state.contacts.map(function(item, idx) {
                        return (<li>{item.contactEmail} {item.contactName}</li>)
                    })}
                    </ul>
                </DialogContent>
            </Dialog>
        </div>
        );
    }
}

export default withStyles(styles)(Navbar);
