import React from 'react';

import ConfigEditor from './ConfigEditor';
import DataManager from './DataManager';

export default class App extends React.Component {
    componentWillMount() {
        DataManager.load();
    }

    render() {
        return (
            <div style={styles.global}>
                <ConfigEditor />
            </div>
        );
    }
};

const styles = {
    global: {
        fontFamily: 'Courier New',
        color: 'white',
    },
};
