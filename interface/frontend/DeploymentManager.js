import React from 'react';
import DeploymentEditor from './DeploymentEditor';
import DataManager from './DataManager';
import NiceButton from './NiceButton';

export default class DeploymentManager extends React.Component {
    _deregister = undefined;

    state = {
        selectedDeployment: -1,
    };

    componentWillMount() {
        this._deregister = DataManager.registerListener(this.onDataChanged.bind(this));
        this.onDataChanged();
    }

    componentWillUnmount() {
        if (this._deregister) {
            this._deregister();
            this._deregister = undefined;
        }
    }

    onDataChanged() {
        this.forceUpdate();
    }

    render() {
        const { selectedDeployment } = this.state;
        const { config } = this.props;

        var deploymentList = DataManager.getConfigDeployments(config).map(deployment =>
            <NiceButton
                    key={"deployment-listitem-"+deployment.id}
                    isHighlighted={selectedDeployment == deployment.id}
                    onClick={() => this.setState({selectedDeployment: deployment.id})} >
                {deployment.target}
            </NiceButton>
        );

        var contentView = null;
        if (selectedDeployment >= 0) {
            contentView = <DeploymentEditor deployment={DataManager.getDeploymentById(selectedDeployment)} />
        } else if (deploymentList.length == 0) {
            deploymentList = <div>None</div>
        }

        return (
            <div style={styles.container}>
                <div style={styles.sidebar}>
                    {deploymentList}
                </div>
                <div style={styles.contentContainer}>
                    {contentView}
                </div>
            </div>
        );
    }
};

const styles = {
    container: {
        display: 'flex',
        flex: 1,
        flexDirection: 'row',
    },
    sidebar: {
        flex: 2,
        flexDirection: 'column',
        maxWidth: 300,
    },
    contentContainer: {
        flex: 3,
    }
};
