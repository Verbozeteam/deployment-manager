import React from 'react';
import NiceButton from './NiceButton';

export default class BlueprintEditor extends React.Component {
    _thingObjects = {
        light_switches: {

            fields: {
                switch_port: {
                    required: true,
                    type: "port",
                },
            },
        },
        dimmers: {
            fields: {
                dimmer_port: {
                    required: true,
                    type: "port",
                },
            },
        },
    };

    state = {
        curJSON: {},
        isLegacyJSON: false,
        curRoomIndex: -1,
        curGroupIndex: -1,
    };

    renderHeader() {
        return (
            <div style={styles.headerContainer}>
                {Object.keys(this._thingObjects).map((t, i) => <NiceButton key={'th-'+i}>{"+ " + t}</NiceButton>)}
            </div>
        );
    }

    renderBlueprint() {
        return <div />;
    }

    translateConfig(config) {
        return config;
    }

    save() {
        this.props.onChange(this.state.isLegacyJSON ? this.translateConfig(this.state.curJSON) : this.state.curJSON);
    }

    render() {
        const { isEditable } = this.props;

        return (
            <div style={styles.container}>
                {isEditable ? this.renderHeader() : null}
                {this.renderBlueprint()}
            </div>
        );
    }
};

const styles = {
    container: {
        flex: 1,
        display: 'flex',
        flexDirection: 'column',
    },
    headerContainer: {
        flex: 1,
        display: 'block',
        backgroundColor: 'red',
    }
};
