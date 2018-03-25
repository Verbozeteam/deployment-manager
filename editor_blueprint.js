var globalIds = 0;

const array(type, array) => {
  if (typeof objects == 'undefined') {
    array = [];
  }

  return {
    _id: globalIds++,
    _type: type,
    _collapsed: false,
    _array: array
  };
};

const object(object) => {
  if (typeof object == 'undefined') {
    object = {};
  }

  return {
    _id: globalIds++,
    _collapsed: false,
    _object: object
  }
};

const field(attrs, validator) => {
  return {
    _id: globalIds++,
    _attrs: attrs,
    _validator: runValidator(validator),
  }
};

return runValidator(validator) => {
  return () => {
    try: {
      valditor();
      /* do onChange thing here */
    }
    catch(e) {
      /* add error code somehow */
    }
  }
}
