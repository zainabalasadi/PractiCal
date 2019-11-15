import React from 'react';
import Button from '@material-ui/core/Button';
import Menu from '@material-ui/core/Menu';
import MenuItem from '@material-ui/core/MenuItem';
import Badge from '@material-ui/core/Badge';
import NotificationsIcon from '@material-ui/icons/Notifications';
import IconButton from '@material-ui/core/IconButton';

export default function Notification() {
  const [anchorEl, setAnchorEl] = React.useState(null);

  const handleClick = event => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <div>
        <IconButton aria-label="show 5 new notifications" color="inherit" onClick={handleClick}>
            <Badge badgeContent={5} color="secondary">
                <NotificationsIcon />
            </Badge>
        </IconButton>

      <Menu
        id="simple-menu"
        anchorEl={anchorEl}
        keepMounted
        open={Boolean(anchorEl)}
        onClose={handleClose}
      >
        <MenuItem onClick={handleClose}>Notification</MenuItem>
        <MenuItem onClick={handleClose}>Notification</MenuItem>
        <MenuItem onClick={handleClose}>Notification</MenuItem>
      </Menu>
    </div>
  );
}