# Sunrice - Garden Light Controller

Sunrice is a quick and dirty Python app for controlling my garden lights. It schedules on/off sequence at sunset/dawn, whereas exact times are calculated on daily basis. MQTT messages are sent to the PLC controller as a on/off sequence. Sunrice also reacts to `sunrise/on` and `sunrise/off` MQTT messagess (with no payload) to start the sequence manually.

## Contributing

Please read [**CONTRIBUTING.md**](https://github.com/hubpav/sunrice/blob/master/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [**SemVer**](https://semver.org/) for versioning. For the versions available, see the [**tags on this repository**](https://github.com/hubpav/sunrice/tags).

## Authors

* [**Pavel Hübner**](https://github.com/hubpav) - Initial work

## License

This project is licensed under the [**MIT License**](https://opensource.org/licenses/MIT/) - see the [**LICENSE**](https://github.com/hubpav/sunrice/blob/master/LICENSE) file for details.
