import React from 'react';
import DataManager from './DataManager';
import NiceButton from './NiceButton';

export default class DeploymentForm extends React.Component {
    state = {
        burnFirmware: false,
        firmware: 1,
        target: "",
        comment: "",
        params: [],
        options: {},
    };

    resetState(config) {
        var _params = DataManager.getConfigFiles(config, true).map(f => DataManager.getConfigFileParameters(f));
        var params = [];
        for (var i = 0; i < _params.length; i++)
            params = params.concat(_params[i]);

        var repositories = DataManager.getConfigRepositories(config, true);
        var buildOptions = [];
        for (var i = 0; i < repositories.length; i++)
            buildOptions = buildOptions.concat(DataManager.getRepositoryBuildOptions(repositories[i].repo));
        var boDict = {};
        for (var i = 0; i < buildOptions.length; i++)
            boDict[buildOptions[i].option_name] = {...buildOptions[i], isChecked: false};

        this.setState({
            burnFirmware: false,
            firmware: DataManager.getAllFirmwares()[0].id,
            target: "",
            comment: "",
            params: params,
            options: boDict,
        })
    }

    componentWillMount() {
        this.resetState(this.props.config);
    }

    componentWillReceiveProps(nextProps) {
        this.resetState(nextProps.config);
    }

    deploy() {
        const { config } = this.props;
        const { firmware, target, comment, params, burnFirmware, options } = this.state;

        if (target.trim() == "") {
            console.log("Missing 'target'");
            return;
        }

        for (var i = 0; i < params.length; i++) {
            if (params[i].parameter_value.trim() == "") {
                console.log("Missing parameter '" + params[i].parameter_name + "'");
                return;
            }
        }

        var optionIds = Object.keys(options).filter(o => o.isChecked).map(o => options[o].id);
        DataManager.deploy(config, burnFirmware ? firmware : -1, target, comment, params, optionIds);
    }

    render() {
        const { config } = this.props;
        const { firmware, target, comment, params, burnFirmware, options } = this.state;

        var firmwareList = DataManager.getAllFirmwares().map(f => <option key={'opf-'+f.id} value={f.id}>{f.local_path}</option>);

        return (
            <div style={styles.container}>
                <div style={styles.row}>
                    <div style={styles.fieldName}>Firmware</div>
                    <div style={styles.fieldValue}>
                        <input type={"checkbox"} checked={burnFirmware} onChange={e => this.setState({burnFirmware: e.target.checked})} />
                        <select>{firmwareList}</select>
                    </div>
                </div>
                <div style={styles.row}>
                    <div style={styles.fieldName}>Target Name</div>
                    <input style={styles.fieldValue} value={target} onChange={e => this.setState({target: e.target.value})} />
                </div>
                <div style={styles.row}>
                    <div style={styles.fieldName}>Comment</div>
                    <textarea style={styles.fieldValue} value={comment} onChange={e => this.setState({comment: e.target.value})} rows={4} />
                </div>
                <div style={styles.row}>
                    <div style={styles.fieldName}>Build options:</div>
                    <div style={styles.fieldValue}></div>
                </div>
                {Object.keys(options).map(option_name =>
                    <div key={'bo-'+option_name} style={styles.row}>
                        <div style={styles.fieldName}>{option_name}</div>
                        <input style={styles.fieldValue} type={"checkbox"} checked={options[option_name].isChecked} onChange={e => this.setState({options: {...options, [option_name]: {...options[option_name], isChecked: e.target.checked}}})} />
                    </div>
                )}
                <div style={styles.row}>
                    <div style={styles.fieldName}>Parameters:</div>
                    <div style={styles.fieldValue}></div>
                </div>
                {params.map((p, i) =>
                    <div key={'dep-param-'+p.parameter_name} style={styles.row}>
                        <div style={styles.fieldName}>{p.parameter_name + " (" + (p.is_required? "required" : "not required") + ")"}</div>
                        <input style={styles.fieldValue} value={p.parameter_value} onChange={(e => {
                            params[i].parameter_value = e.target.value;
                            this.setState({params});
                        }).bind(this)} />
                    </div>
                )}
                <div style={styles.row}>
                    <div style={styles.fieldName}></div>
                    <div style={styles.fieldValue}>
                        <NiceButton
                                onClick={this.deploy.bind(this)} >
                            Deploy
                        </NiceButton>
                    </div>
                </div>
            </div>
        );
    }
};

const styles = {
    container: {
        display: 'flex',
        flexDirection: 'column',
        flex: 1,
    },
    row: {
        display: 'flex',
        flexDirection: 'row',
        margin: 10,
    },
    fieldName: {
        fontWeight: 'bold',
        color: '#ba3737',
        flex: 1,
        textAlign: 'right',
        marginRight: 20,
    },
    fieldValue: {
        flex: 3,
    },
};

