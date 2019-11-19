import React from 'react';
import Button from '@material-ui/core/Button';
import Menu from '@material-ui/core/Menu';
import MenuItem from '@material-ui/core/MenuItem';
import Badge from '@material-ui/core/Badge';
import { withStyles } from "@material-ui/core/styles";
import NotificationsIcon from '@material-ui/icons/Notifications';
import IconButton from '@material-ui/core/IconButton';

const styles = theme => ({

});

class Notification extends React.Component {
  	state = {
    	anchorEl: null,
  	};

  	handleClick = event => {
    	this.setState({ anchorEl: event.currentTarget });
  	};

  	handleClose = () => {
    	this.setState({ anchorEl: null });
  	};

  	render() {
		return (
			<div>
				<IconButton aria-label="show 5 new notifications" color="inherit" onClick={this.handleClick}>
					<Badge badgeContent={5} color="secondary">
						<NotificationsIcon />
					</Badge>
				</IconButton>

			<Menu
				id="simple-menu"
				anchorEl={this.state.anchorEl}
				keepMounted
				open={Boolean(this.state.anchorEl)}
				onClose={this.handleClose}
			>
				<MenuItem onClick={this.handleClose}>Notification</MenuItem>
				<MenuItem onClick={this.handleClose}>Notification</MenuItem>
				<MenuItem onClick={this.handleClose}>Notification</MenuItem>
			</Menu>
			</div>
		);
	}
}

export default withStyles(styles)(Notification);