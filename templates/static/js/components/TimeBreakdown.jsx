import React, { Component } from "react";
import Button from '@material-ui/core/Button';
import { Dialog, DialogContent, DialogContentText, DialogTitle } from '@material-ui/core';
import CloseIcon from '@material-ui/icons/Close';
import IconButton from '@material-ui/core/IconButton';
import { withStyles } from "@material-ui/core/styles";

const styles = theme => ({
    closeButton: {
        position: 'absolute',
        right: theme.spacing(1),
        top: theme.spacing(1),
    },
    heading: {
        fontSize: 100,
        margin: '20px 0 20px 0',
    }
});

class TimeBreakdown extends Component {
    _isMounted = false;
    constructor() {
        super();
        this.state = {
            // Loading sample events, remove later
            open: false,
            setOpen: false,
            userName: "",
        };
        this.handleClose = this.handleClose.bind(this);
        this.handleClickOpen = this.handleClickOpen.bind(this);
    };

    componentDidMount() {
        this._isMounted = true;
      
        let response = fetch('/getName', {
            method: 'GET'

        }).then((data) => data.json()).then(result => {
            if (this._isMounted) {
                this.setState({userName: result})
            }
        });
    }
    
    componentWillUnmount() {
        this._isMounted = false;
    }

    handleClickOpen() {
        this.setState({ setOpen: true });
    }

    // Closes modal
    handleClose() {
        this.setState({ setOpen: false });
    }

    render() {
        const { classes } = this.props;
        return (
        <div>
            <Button variant="outlined" color="primary" onClick={this.handleClickOpen}>
                TimeBreakdowns test button
            </Button>
            <Dialog
            open={this.state.setOpen}
            onClose={this.handleClose}
            aria-labelledby="alert-dialog-title"
            aria-describedby="alert-dialog-description"
            >
                <IconButton aria-label="close" className={classes.closeButton} onClick={this.handleClose}>
                    <CloseIcon />
                </IconButton>
                <DialogTitle className={classes.heading}>{`Good morning ${this.state.userName},`}</DialogTitle>
                <DialogContent>
                    <DialogContentText>
                        Last week, you spent
                    </DialogContentText>
                </DialogContent>
            </Dialog>
        </div>
        );
    }
}

export default withStyles(styles)(TimeBreakdown);