# Public-release privacy checklist

This project may combine precise geolocation, timestamps, physiological signals,
event annotations, street images, and audio-derived spectrograms.

Before publishing publicly:

- Confirm that participant consent covers public online publication.
- Remove names, device identifiers, account information, and hidden metadata.
- Review whether precise coordinates reveal homes, workplaces, routines, or sensitive places.
- Consider reducing coordinate precision or using synthetic demonstration data.
- Review every street image for faces, license plates, screens, badges, and addresses.
- Strip EXIF metadata from images.
- Confirm that spectrograms and event annotations do not expose private conversations or identities.
- Publish only the physiological fields needed for the demonstration.
- Check Git history before making the repository public; deleting a file later does not erase old commits.
- Use only a restricted Mapbox public token in browser code.

This checklist is a practical publication aid and is not legal advice.
