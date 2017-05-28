lint:
	pylint src/*py --max-line-length=120 --generated-members=fields,flags,__name__,dwHeight,dwWidth,dwMagic,dwFourCC --msg-template='{msg_id}:{line:3d},{column}: {obj}: {msg}' -d W0631,C0413 && echo "LINT PASSED" || echo "LINT FAILED."
