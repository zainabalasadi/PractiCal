import React from 'react';
import Button from '@material-ui/core/Button';
import Menu from '@material-ui/core/Menu';
import MenuItem from '@material-ui/core/MenuItem';
import Typography from '@material-ui/core/Typography'
import ListItem from '@material-ui/core/ListItem'
import ListItemIcon from '@material-ui/core/ListItemIcon'
import Badge from '@material-ui/core/Badge';
import { withStyles } from "@material-ui/core/styles";
import NotificationsIcon from '@material-ui/icons/Notifications';
import CheckIcon from '@material-ui/icons/Check';
import CloseIcon from '@material-ui/icons/Close';
import IconButton from '@material-ui/core/IconButton';

const styles = theme => ({
    message: {
        fontSize: 14,
        float: 'left',
        marginBottom: theme.spacing(1),
    },
    wrapper: {
        padding: theme.spacing(2, 2, 2, 2),
    },
});

class Notification extends React.Component {
    constructor() {
        super()
        this.state = {
            notifs: [],
            anchorEl: null
        }
    };
    get_notifs() {
        let response = fetch('/getNotifs', {
        method: 'GET'

        }).then((data) => data.json()).then(data => {
            this.setState({notifs: data})
        });
    }

    delete_notif(notif_id) {
      let response = fetch('/deleteNotif', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({"id": notif_id})
        }).then((data) => data.json());
    }

    respond_to_invite(event_id, resp) {
      let response = fetch('/inviteResponse', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({"id": event_id, "response": resp})
        }).then((data) => data.json());
    }

    componentDidMount() {
        this.get_notifs()
    }

  	handleClick = event => {
    	this.setState({ anchorEl: event.currentTarget });
  	};

  	handleClose = event => {
    	this.setState({ anchorEl: null });
  	};

    handleCloseDelete = event => {
        this.delete_notif(event.currentTarget.id)
        this.get_notifs()
        this.handleClose(event)
    }

    handleInviteGoing = event => {
        this.respond_to_invite(event.currentTarget.getAttribute('eid'), "going")
        this.handleCloseDelete(event)
    }

    handleInviteDecline = event => {
        this.respond_to_invite(event.currentTarget.getAttribute('eid'), "decline")
        this.handleCloseDelete(event)
    }

  	render() {
        const { classes } = this.props;
		return (
			<div>
				<IconButton aria-label="show new notifications" color="inherit" onClick={this.handleClick}>
					<Badge badgeContent={this.state.notifs.length} color="secondary">
						<NotificationsIcon />
					</Badge>
				</IconButton>

			<Menu
				id="simple-menu"
				anchorEl={this.state.anchorEl}
				keepMounted
				open={Boolean(this.state.anchorEl)}
                onClose={this.handleClose}
                maxWidth={'xs'}
			>
        {this.state.notifs.map((notif) => {
          if (notif.type === "EVENTINVITE") {
            return (
                <MenuItem className={classes.wrapper} key={notif.id} id={notif.id} onClick={this.handleClose}>
                    <ul>
                    <li>
                        <div className={classes.message} variant="inherit">
                            {notif.message}:
                        </div>
                    </li>
                    <li>
                        <div className="notifEventBlock">
                            <p className="notifTitle">{notif.eTitle}</p>
                            <p className="notifDate">{notif.eStart} - {notif.eEnd}</p>
                            <span>Going?</span>
                            <div style={{ float: 'right' }}>
                                <IconButton id={notif.id} eid={notif.eid} onClick={this.handleInviteGoing}>
                                    <CheckIcon fontSize="small" className="going"/>
                                </IconButton>
                                <IconButton id={notif.id} eid={notif.eid} onClick={this.handleInviteDecline}>
                                    <CloseIcon fontSize="small" className="going"/>
                                </IconButton>
                            </div>
                        </div>
                    </li>
                    </ul>
              </MenuItem>
            )
          } else {
                return (
                    <MenuItem className={classes.wrapper} key={notif.id} id={notif.id} onClick={this.handleCloseDelete}>
                        <ul>
                        <li>
                            <div className={classes.message} variant="inherit">
                                {notif.message}:
                            </div>
                        </li>
                        <li>
                            <div className="notifEventBlock">
                                <p className="notifTitle">{notif.eTitle}</p>
                                <p className="notifDate">{notif.eStart} - {notif.eEnd}</p>
                            </div>
                        </li>
                        </ul>
                    </MenuItem>
                )
            }
        })}
			</Menu>
		</div>
		);
	}
}

export default withStyles(styles)(Notification);
