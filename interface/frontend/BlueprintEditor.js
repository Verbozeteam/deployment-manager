import React from 'react';
import NiceButton from './NiceButton';

export default class BlueprintEditor extends React.Component {

  state = {
    viewType: 'structured', /* either structured or dump (dump == textfield) */
    version: 1,
    blueprint: {},
    fields: {}
  }

  globalIds = 0;

  componentWillMount() {
    this.componentWillReceiveProps(this.props);
  }

  componentWillReceiveProps(nextProps) {
    console.log('componentWillReceiveProps()');
    const { content } = nextProps;

    this.v1ToEditorFormat(content);
  }

  /* create exportable array object in internal format */
  createArray(array, addables) {
    return {
      _type: 'array',
      id: this.globalIds++,
      collapsed: false,
      array,
      addables,
    };
  }

  /* create exportable Javascript object object in internal format */
  createObject(object) {
    return {
      _type: 'object',
      id: this.globalIds++,
      collapsed: false,
      object
    };
  }

  /* create exportable editor fields object in internal format */
  createField(value, type, validator, editable) {
    const { fields } = this.state;

    if (typeof validator == 'undefined') {
      validator = () => {};
    }

    if (typeof editable == 'undefined') {
      editable = true;
    }

    const id = this.globalIds++;

    /* add initial value in fields */
    fields[id] = value;
    this.setState({
      fields: fields
    });

    return {
      _type: 'field',
      id,
      type,
      validator,
      editable
    };
  }

  v1ToEditorFormat(content) {
    console.log('v1ToEditorFormat()', content);

    const v1 = this.parseJson(content);

    const createNameField = (name) => {
      return this.createObject({
        en: this.createField(name.en, 'text'),
        ar: this.createField(name.ar, 'text')
      });
    }

    const blueprint = this.createObject({
      id: this.createField(v1.id, 'number'),
      rooms: this.createArray(v1.rooms.map(room => this.createObject({
        name: this.createField(room.name, 'text'),
        grid: this.createArray(room.grid.map(grid => this.createObject({
          ratio: this.createField(grid.ratio, 'number'),
          panels: this.createArray(grid.panels.map(panel => this.createObject({
            ratio: this.createField(panel.ratio, 'number'),
            name: createNameField(panel.name),
            things: this.createArray(panel.things.map(thing => this.createObject({
              category: this.createField(thing.category, 'text'),
              name: createNameField(thing.name),
            })), 'Thing')
          })), 'Panel')
        })), 'Grid'),
        detail: this.createObject({
          ratio: this.createField(room.detail.ratio, 'number'),
          side: this.createField(room.detail.side, 'text')
        }),
        layout: this.createObject({
          margin: this.createField(room.layout.margin, 'number')
        })
      })), 'Room')
    });

    this.setState({
      blueprint
    });
  }

  // TODO: implement this
  v2ToEditorFormat(blueprint) {
  }

  // TODO: implement this
  editorFormatToV1() {
  }

  // TODO: implement this
  editorFormatToV2() {
  }

  renderViewTypeButtons() {
    const { viewType, version } = this.state;

    return (
      <div style={styles.horizontal_flex}>
        <NiceButton onClick={() => this.setState({viewType: 'structured'})}
            extraStyle={{display: 'flex', flex: 1}}
            isHighlighted={viewType === 'structured'}>
            {'structured'}
            <form>
                <input type={'radio'}
                    checked={version === 1}
                    onChange={() => this.setState({version: 1})} />v1
                <input type={'radio'}
                    checked={version === 2}
                    onChange={() => this.setState({version: 2})} />v2
            </form>
        </NiceButton>
        <NiceButton onClick={() => this.setState({viewType: 'dump'})}
            extraStyle={{display: 'flex', flex: 1}}
            isHighlighted={viewType === 'dump'}>
            {'dump'}
        </NiceButton>
      </div>
    );
  }

  renderV1Editor() {
    const { blueprint } = this.state;

    console.log('renderV1Editor()', blueprint);
  }

  renderDumpEditor(blueprint) {
    const { content, editable, onChange } = this.props;

    return (
      <textarea style={{width: '100%'}}
        disabled={!editable}
        value={content}
        onChange={e => onChange({content: e.target.value})}
        rows={35} />
    );
  }

  // TODO: implement this
  parseJson(json_string) {
    var index = json_string.indexOf('{{');
    // FIXME: this will alwasy be stuck at the first occurrence
    while (index !== -1 && json_string[index-1] !== '\"') {
      json_string = json_string.replace('{{', '\"{{');
      json_string = json_string.replace('}}', '}}\"');
      var index = json_string.indexOf('{{');
    }
    return JSON.parse(json_string);
  }

  render() {
    const { content } = this.props;
    const { viewType, version } = this.state;

    var editor = null;
    if (viewType === 'structured') {
      if (version === 1) {
        editor = this.renderV1Editor();
      }
    }

    else {
      editor = this.renderDumpEditor(content);
    }

    return (
      <React.Fragment>
        <h3>Blueprint Editor</h3>
        {this.renderViewTypeButtons()}
        <hr />
        {editor}
      </React.Fragment>
    );
  }
}

const styles = {
    horizontal_flex: {
        display: 'flex',
        flex: 1,
        flexDirection: 'row'
    },
    node: {
        // width: '100%',
        border: '1px solid #BA3737',
        backgroundColor: 'rgba(186, 55, 55, 0.1)',
        padding: 20,
        paddingRight: 0,
        marginTop: 5,
        marginBottom: 5
    }
};
