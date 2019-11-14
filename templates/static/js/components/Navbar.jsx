import React, { Component } from "react";
import { fade } from '@material-ui/core/styles';
import { AppBar, Toolbar, InputBase } from '@material-ui/core';
import { Dialog, DialogTitle, DialogContent, Button, TextField, Typography } from "@material-ui/core";
import IconButton from '@material-ui/core/IconButton';
import Badge from '@material-ui/core/Badge';
import SearchIcon from '@material-ui/icons/Search';
import CloseIcon from '@material-ui/icons/Close';
import AccountCircle from '@material-ui/icons/AccountCircle';
import NotificationsIcon from '@material-ui/icons/Notifications';
import PeopleIcon from '@material-ui/icons/People';
import logo from '../../../public/logo.svg';
import { withStyles } from "@material-ui/core/styles";
import TimeBreakdown from './TimeBreakdown'

const navHeight = 64;

const styles = theme => ({
    nav: {
        zIndex: '1400',
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
    constructor() {
        super();
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
            groupName: "",
            groupEmail: "",
            contactName: "",
            contactEmail: "",
            openContacts: false,
            openNotification: false,
        };
        this.handleClose = this.handleClose.bind(this);
        this.handleContactOpen = this.handleContactOpen.bind(this);
    };

    search() {
        let response = fetch('/searchEvent', {
            method: 'POST',
            body: JSON.stringify({"queryString": searchText}),
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            }
        }).then(response => response.json()).then(data => console.log(data))
        // TODO Insert code to change state of front end given response from the back end
    }

    // Function to create contact and send to back-end
    create_contact(contact) {
        console.log(contact)
        
    }

    // Function to create group and send to back-end
    create_group(group) {
        console.log(group)
        
    }

    setNewContact() {
        const { contactName, contactEmail } = this.state;
        let newContact = { contactName, contactEmail };
        let contacts = this.state.contacts.slice();
        contacts.push(newContact);
        this.setState({ contacts });
        this.create_contact(newContact)
    }

    setNewContact() {
        const { groupName, groupEmail } = this.state;
        let newGroup = { groupName, groupEmail };
        let groups = this.state.groups.slice();
        groups.push(newGroup);
        this.setState({ groups });
        this.create_group(newGroup)
    }

    // Sets the state of input
    setContactEmail = e => { 
        this.setState({ contactEmail: e }); 
    };
    setContactName = e => { 
        this.setState({ contactName: e }); 
    };
    setGroupEmail = e => { 
        this.setState({ groupEmail: e }); 
    };
    setGroupName = e => { 
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
                        fullWidth='true'
                        placeholder="Search"
                        classes={{
                            root: classes.inputRoot,
                            input: classes.inputInput,
                        }}
                        inputProps={{ 'aria-label': 'search' }}
                        name="search"
                        // value={searchText}
                        onChange={e => {
                            // setSearchText(e.target.value)
                            // console.log(searchText)
                        }}
                        onKeyPress={e => {
                            if (e.key === "Enter") {
                            search()
                            }
                        }}
                        />
                    </div>
                    <TimeBreakdown/>
                    <div className={classes.grow} />
                    <div className={classes.sectionDesktop}>
                        <IconButton aria-label="show 5 new notifications" color="inherit">
                            <Badge badgeContent={5} color="secondary">
                                <NotificationsIcon />
                            </Badge>
                        </IconButton>
                        <IconButton color="inherit"
                            onClick={this.handleContactOpen}
                        >
                            <PeopleIcon />
                        </IconButton>
                        <IconButton  color="inherit">
                            <AccountCircle />
                        </IconButton>
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
                        onChange={this.setGroupName}
                    />
                    <TextField 
                        placeholder="Emails"
                        margin="dense"
                        onChange={this.setGroupEmail}
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
                        onChange={this.setContactName}
                    />
                    <TextField 
                        placeholder="Email"
                        margin="dense"
                        onChange={this.setContactEmail}
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

                </DialogContent>
            </Dialog>
        </div>
        );
    }
}

export default withStyles(styles)(Navbar);
