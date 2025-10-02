module.exports = {
  plugins: {
    'postcss-preset-mantine': {},
    'postcss-simple-vars': {
      variables: {
        'mantine-breakpoint-xs': '36em',
        'mantine-breakpoint-sm': '48em',
        'mantine-breakpoint-md': '62em',
        'mantine-breakpoint-lg': '75em',
        'mantine-breakpoint-xl': '88em',
        'mantine-breakpoint-2xl': '96em',
        'mantine-breakpoint-3xl': '108em',  // 1728px
        'mantine-breakpoint-4xl': '120em',  // 1920px
      },
    },
  },
};