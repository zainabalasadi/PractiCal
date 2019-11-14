import React from 'react';
import Button from '@material-ui/core/Button';
import { Typography, Dialog, DialogContent, DialogContentText, DialogTitle } from '@material-ui/core';
import CloseIcon from '@material-ui/icons/Close';
import { makeStyles } from '@material-ui/core/styles';
import IconButton from '@material-ui/core/IconButton';

const useStyles = makeStyles(theme => ({
    closeButton: {
        position: 'absolute',
        right: theme.spacing(1),
        top: theme.spacing(1),
    },
    heading: {
        fontSize: 100,
        margin: '20px 0 20px 0',
    }
}));

export default function TimeBreakdown() {
    const classes = useStyles();
    const [open, setOpen] = React.useState(false);

    const handleClickOpen = () => {
        setOpen(true);
    };

    const handleClose = () => {
        setOpen(false);
    };

    return (
    <div>
        <Button variant="outlined" color="primary" onClick={handleClickOpen}>
            TimeBreakdowns test button
        </Button>
        <Dialog
          open={open}
          onClose={handleClose}
          aria-labelledby="alert-dialog-title"
          aria-describedby="alert-dialog-description"
        >
            <IconButton aria-label="close" className={classes.closeButton} onClick={handleClose}>
                <CloseIcon />
            </IconButton>
            <DialogTitle className={classes.heading}>{"Good morning User,"}</DialogTitle>
            <DialogContent>
                <DialogContentText>
                    Last week, you spent
                </DialogContentText>
            </DialogContent>
        </Dialog>
    </div>
    );
}